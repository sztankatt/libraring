from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import get_template
from django.template import Context

from usr.project import user_is_not_blocked
from books.forms import BookForm, OfferForm
from books.models import Book, Genre, Author, Publisher, Offer, Transaction, TransactionRating


@login_required
@ensure_csrf_cookie 
@user_is_not_blocked
def main_page(request):
    form = BookForm()
            
    return render(request, 'after_login/books/main_page.html', {'form': form})

@login_required
def book_page(request, id=None):
    if id is None:
        return Http404()
    else:
        offer_form = None
        book = get_object_or_404(Book, pk=id)
        offers = Offer.objects.filter(book=book).order_by('-offered_price')
        #if the book is not sold, proceed
        if book.is_sold() is None:
            if request.user != book.user:
                offer_form = OfferForm({'book':book.id, 'made_by':request.user.id})
        
        return render(request, 'after_login/books/book_page.html', {
            'book':book, 
            'user':request.user,
            'offers':offers,
            'offer_form':offer_form})

@login_required
@user_is_not_blocked
def genre(request, name):
	try:
		genre = Genre.objects.get(name=name)

		book_list = genre.book_set.all()

		return render(request, 'after_login/books/show_books.html', {'books':book_list, 'genre':genre, 'type':'genre'})
	except Genre.DoesNotExist:
		raise Http404

@login_required
@user_is_not_blocked
def author(request, pk):
    try:
        author = Author.objects.get(pk=pk)

        book_list = author.book_set.all()

        return render(request, 'after_login/books/show_books.html', {'books':book_list, 'author':author, 'type':'author'})

    except Author.DoesNotExist:
        raise Http404


@login_required
@user_is_not_blocked
def publisher(request, pk):

    try:
        publisher = Publisher.objects.get(pk=pk)

        book_list = publisher.book_set.all()

        return render(request, 'after_login/books/show_books.html', {'books':book_list, 'publisher':publisher, 'type':'publisher'})



    except Publisher.DoesNotExist:
        raise Http404

@login_required
@user_is_not_blocked
def make_an_offer(request):
    if request.is_ajax() and request.method == 'POST':
        form = OfferForm(request.POST)

        if form.is_valid():
            offer = form.save()

            book = offer.book
            book.status = 'offered'
            book.save()

            template = get_template('after_login/books/book_offer.html')

            context = Context({'offer':offer})

            output = template.render(context)

            return HttpResponse(output)
    else:
        raise Http404

@login_required
@user_is_not_blocked
def accept_the_offer(request):
    if request.method == 'POST':
        offer_id = request.POST.get('offer_id', False)

        if offer_id == False:
            raise Http404



        transaction = Transaction()
        transaction.save()

        #geting the offer and marking as accepted
        offer = Offer.objects.get(pk=offer_id)
        offer.accepted = True
        offer.transaction = transaction
        offer.save()

        #getting the book
        book = offer.book

        #updating the book
        book.sold_to = offer.made_by
        book.status = 'selling'
        book.save()


        #redirect to the page of the book
        return HttpResponseRedirect(reverse('books:book_page', args=(book.id,)))


    else:
        raise Http404


    return HttpResponse(post)


@login_required
@user_is_not_blocked
def finalise_transaction(request):
    if request.method == 'POST':
        seller = request.POST.get('seller', None)
        transaction_id = request.POST.get('transaction', None)
        user = request.user

        if seller == None or transaction_id == None:
            raise Http404

        transaction = Transaction.objects.get(pk=int(transaction_id))

        book = transaction.offer.book

        if seller == 'true':
            transaction.finalised_by_seller = True
            transaction.save()
        elif seller == 'false':
            transaction.finalised_by_buyer = True
            transaction.save()
        else:
            raise Http404

        if transaction.finalised_by_buyer and transaction.finalised_by_seller:
            if seller == 'true':
                seller = user
                buyer = transaction.offer.made_by
            else:
                seller = transaction.offer.made_by
                buyer = user

            tr = TransactionRating(buyer=buyer, seller=seller)
            tr.save()

            #change the status of the book
            book.status = 'finalised'
            book.save()

            transaction.rating = tr
            transaction.save()


        return HttpResponseRedirect(reverse('books:book_page', args=(book.id,)))

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
                #rate the buyer
                tr.buyer_rating = rating
                tr.save()
            elif user.id == tr.buyer.id:
                #rate the seller
                tr.seller_rating = rating
                tr.save()
            else:
                #not in the tr
                raise Http404

            return HttpResponseRedirect(reverse('books:book_page', args=(tr.transaction.offer.book.id,)))


        except TransactionRating.DoesNotExist:
            raise Http404

    else:
        raise Http404

    #TODO: possible cleanup of unused methods
    #TODO: check if book status is correct every time
    #TODO: send an email to the user actually
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

            #TODO: delete this from conversation and add to book

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

        return render(request, 'after_login/books/transaction_rate.html', {'selling':selling, 'tr':tr})


    except Transaction.DoesNotExist:
        raise Http404