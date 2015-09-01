from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.template.loader import get_template
from django.template import Context
from django.core import mail
from django.utils.translation import ugettext as _
from django.db.models import Q


from usr.project import user_is_not_blocked
from books.forms import OfferForm, BookStatusForm
from books.models import Book, Genre, Author, Publisher,\
    Offer, Transaction, TransactionRating, BoughtBook
from usr.signals import *


@login_required
@ensure_csrf_cookie
@user_is_not_blocked
def usr_book_page(request, type='books'):
    out = {
        'type': type,
        'books': None,
        'form': OfferForm({
            'made_by': request.user
        })
    }

    if type == 'books':
        out['book_status_form'] = BookStatusForm(request.GET)
        statuses = request.GET.getlist('book_status')

        books = Book.objects.all()
        books = books.filter(user=request.user)

        if statuses:
            flt = Q()
            for status in statuses:
                flt = flt | Q(status=status)

            books = books.filter(flt).distinct()

    elif type == 'offers':
        books = set([x.book for x in request.user.offer_set.all()])

    elif type == 'watchlist':
        books = [x.book for x in request.user.watchlist_set.all()]

    out['books'] = books

    return render(request, 'after_login/books/usr_books.html', {'data': out})


@login_required
def book_page(request, id=None):
    if id is None:
        return Http404()
    else:
        offer_form = None
        book = get_object_or_404(Book, pk=id)
        offers = Offer.objects.filter(book=book).order_by('-offered_price')
        # if the book is not sold, proceed
        if book.is_sold() is False:
            if request.user != book.user:
                offer_form = OfferForm({
                    'book': book.id,
                    'made_by': request.user.id
                })

        return render(request, 'after_login/books/book_page.html', {
            'book': book,
            'user': request.user,
            'offers': offers,
            'offer_form': offer_form})


@login_required
@user_is_not_blocked
def genre(request, name):
    try:
        genre = Genre.objects.get(name=name)

        book_list = genre.book_set.all()

        return render(request, 'after_login/books/show_books.html',
                      {'books': book_list, 'genre': genre, 'type': 'genre'})
    except Genre.DoesNotExist:
        raise Http404


@login_required
@user_is_not_blocked
def author(request, pk):
    try:
        author = Author.objects.get(pk=pk)

        book_list = author.book_set.all()

        return render(request, 'after_login/books/show_books.html',
                      {'books': book_list, 'author': author, 'type': 'author'})

    except Author.DoesNotExist:
        raise Http404


@login_required
@user_is_not_blocked
def publisher(request, pk):
    try:
        publisher = Publisher.objects.get(pk=pk)

        book_list = publisher.book_set.all()

        return render(
            request, 'after_login/books/show_books.html',
            {'books': book_list, 'publisher': publisher, 'type': 'publisher'})

    except Publisher.DoesNotExist:
        raise Http404


@login_required
@user_is_not_blocked
def make_an_offer(request):
    user_id = request.POST.get('made_by', None)
    if user_id is None or (int(user_id) != int(request.user.pk)):
        raise Http404

    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['book'].get_highest_offer() is not None:
                previous_highest = {
                    'price': form.cleaned_data['book'].get_highest_offer(
                    ).offered_price,
                    'user': form.cleaned_data['book'].get_highest_offer(
                        ).made_by
                }
            else:
                previous_highest = None

            try:
                offer = Offer.objects.get(
                    made_by=request.user, book=form.cleaned_data['book'])
                offer.offered_price = form.cleaned_data['offered_price']
                offer.save()
                changed_offer = True
            except Offer.DoesNotExist:
                offer = form.save()
                changed_offer = False

            # signals
            # if same offer
            if previous_highest is not None:
                if changed_offer:
                    if (offer.offered_price >= previous_highest['price'] and
                            offer.made_by.pk != previous_highest['user'].pk):
                        new_highest_offer.send(
                            sender=offer.user.__class__,
                            offer=offer,
                            user=request.user,
                            previous_highest=previous_highest['price'],
                            previous_user=previous_highest['user'],
                            book=offer.book)
                else:
                    if offer.offered_price >= previous_highest['price']:
                        new_highest_offer.send(
                            sender=offer.user.__class__,
                            offer=offer,
                            user=request.user,
                            previous_highest=previous_highest['price'],
                            previous_user=previous_highest['user'],
                            book=offer.book)

            book_new_offer.send(sender=Offer, offer=offer)

            book = offer.book
            book.status = 'offered'
            book.save()
    else:
        raise Http404

    if request.method == 'POST' and request.is_ajax():
            template = get_template('after_login/books/book_offer.html')

            context = Context({'offer': offer, 'request': request})

            output = template.render(context)

            return HttpResponse(output)
    else:
            return HttpResponseRedirect(
                reverse('books:book_page', args=(book.id,))
                )


def delete_the_offer(request):
    if request.is_ajax:
        return HttpResponse(request.POST['offer_id'])


def send_accepted_offer_email(seller, buyer, book):
    sender = "LIBRARING: %s accepted your offer <%s>" % (seller.username, seller.email)
    to = buyer.email
    subject = "Your offer for %s has been accepted!" % book

    text_content = get_template("after_login/books/accepted_offer_email.txt")
    html_content = get_template("after_login/books/accepted_offer_email.html")

    d = Context({"seller": seller, "buyer": buyer, "book": book})

    text_content = text_content.render(d)
    html_content = html_content.render(d)

    m = mail.EmailMultiAlternatives(subject, text_content, sender, [to])
    m.attach_alternative(html_content, 'text/html')
    m.send()


@login_required
@user_is_not_blocked
def accept_the_offer(request):
    if request.method == 'POST':
        offer_id = request.POST.get('offer_id', False)

        if offer_id is False:
            raise Http404

        # geting the offer and marking as accepted
        offer = get_object_or_404(Offer, pk=offer_id)

        if request.user != offer.book.user:
            raise Http404

        transaction = Transaction()
        transaction.save()
        offer.accepted = True
        offer.transaction = transaction
        offer.save()

        # getting the book
        book = offer.book

        # updating the book
        book.sold_to = offer.made_by
        book.status = 'selling'
        book.save()

        # Seding the email to buyer
        # send_accepted_offer_email(book.user, book.sold_to, book)
        accepted_offer.send(
            sender=book.user.__class__,
            seller=book.user,
            buyer=book.sold_to,
            book=book)

        # redirect to the page of the book
        return HttpResponseRedirect(reverse(
            'books:book_page', args=(book.id,)))

    else:
        raise Http404

    return HttpResponse(post)


@login_required
@user_is_not_blocked
def finalise_transaction(request):
    if request.method == 'POST':
        transaction_id = request.POST.get('transaction', None)
        user = request.user

        if transaction_id is None:
            raise Http404

        transaction = Transaction.objects.get(pk=int(transaction_id))

        finalised_by_seller = False

        if request.user == transaction.offer.book.user:
            seller = request.user
            buyer = transaction.offer.made_by
            finalised_by_seller = True
        elif request.user == transaction.offer.made_by:
            seller = transaction.offer.book.user
            buyer = request.user
        else:
            raise Http404

        book = transaction.offer.book

        if finalised_by_seller:
            transaction.finalised_by_seller = True
            transaction.save()
        else:
            transaction.finalised_by_buyer = True
            transaction.save()

        if transaction.finalised_by_buyer and transaction.finalised_by_seller:
            tr = TransactionRating(buyer=buyer, seller=seller)
            tr.save()

            # change the status of the book
            book.status = 'finalised'
            book.save()

            transaction.rating = tr
            transaction.save()

            BoughtBook.objects.create(
                user=transaction.offer.made_by,
                book=book,
                accepted_price=transaction.offer.offered_price)

            book_finalised_by_other_user.send(
                sender=transaction.__class__,
                finalised_by_seller=finalised_by_seller,
                seller=seller,
                buyer=buyer,
                transaction=transaction)
        else:
            book_finalised_by_other_user.send(
                sender=user.__class__,
                finalised_by_seller=finalised_by_seller,
                seller=seller,
                buyer=buyer,
                transaction=transaction)

        # sending a signal, which will be handled in signal.py

        return HttpResponseRedirect(reverse(
            'books:book_page', args=(book.id,)))

    else:
        raise Http404


@login_required
@user_is_not_blocked
def rate_transaction(request):
    if request.method == 'POST':
        tr_id = request.POST.get('tr_id', None)
        rating = request.POST.get('rating', None)
        user = request.user

        if tr_id == None or rating == None:
            raise Http404

        try:
            tr = TransactionRating.objects.get(pk=tr_id)

            if user.id == tr.seller.id:
                # rate the buyer
                tr.buyer_rating = rating
                tr.save()
            elif user.id == tr.buyer.id:
                # rate the seller
                tr.seller_rating = rating
                tr.save()
            else:
                # not in the tr
                raise Http404

            return HttpResponseRedirect(reverse('books:book_page', args=(tr.transaction.offer.book.id,)))


        except TransactionRating.DoesNotExist:
            raise Http404

    else:
        raise Http404

        # TODO: possible cleanup of unused methods
        # TODO: check if book status is correct every time
        # TODO: send an email to the user actually


"""
    NOT USED
"""


@login_required
@user_is_not_blocked
def transaction_accept(request):
    if request.method == 'POST':
        transaction_id = request.POST.get('transaction', None)
        user_id = request.POST.get('user_id', None)

        user = request.user

        if transaction_id == None or user_id == None:
            raise Http404

        if user.id != int(user_id):
            raise Http404

        try:
            transaction = Transaction.objects.get(pk=transaction_id)

            if user.id == transaction.offer.book.user.id:
                seller = True
            elif user.id == transaction.offer.made_by.id:
                seller = False
            else:
                raise Http404

            if seller:
                transaction.finalised_by_seller = True
                transaction.save()

            else:
                transaction.finalised_by_buyer = True
                transaction.save()

            if transaction.finalised_by_buyer and transaction.finalised_by_seller:
                return HttpResponseRedirect(reverse('user_messages:transaction_rate', args=(transaction_id,)))
            else:
                return HttpResponseRedirect(reverse('user_messages:conversation', args=(transaction_id,)))


        except Transaction.DoesNotExist:
            raise Http404

    else:
        raise Http404


"""
    NOT USED
"""


@login_required
@user_is_not_blocked
def transaction_rate(request, pk):
    user = request.user

    try:
        transaction = Transaction.objects.get(pk=pk)

        if user.id == transaction.offer.book.user.id:
            seller = user
            buyer = transaction.offer.made_by
            selling = True
        elif user.id == transaction.offer.made_by.id:
            seller = transaction.offer.book.user
            buyer = user
            selling = False
        else:
            raise Http404

        obj, created = TransactionRating.objects.get_or_create(transaction=transaction, seller=seller, buyer=buyer)

        tr = obj

        return render(request, 'after_login/books/transaction_rate.html', {'selling': selling, 'tr': tr})


    except Transaction.DoesNotExist:
        raise Http404