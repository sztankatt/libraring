#django
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Max

#python
import json
import datetime

#project
from usr.models import Institution, PageMessages, EmailChange
from usr.project import ProfileUpdate, NoCurrentSchoolError, InvalidSchoolYears, ClassDoesNotExists,\
    NotPreviousEducation

from books.models import WatchList, Offer, Transaction, Book, TransactionRating, Publisher
from books.forms import BookForm

from user_messages.models import Message

from notifications.models import Notification

def get_email_ending(request):
    if request.is_ajax():
        id = request.GET['id']
        
        institution = Institution.objects.get(pk=id)
        
        return HttpResponse(institution.email_ending)
    else: raise Http404
        
        
def check_email_ending(request):
    success = False
    if request.is_ajax():
        try:
            institution_id = request.GET['institution']
            
            
            if institution_id != "":
                try:
                    i = Institution.objects.get(pk=institution_id)
                    
                    try:
                        email = request.GET['class-email']
                    except KeyError:
                        email = request.GET['email']
                    
                    
                    
                    if email.endswith(i.email_ending):
                        success = True
                    
                    return HttpResponse(json.dumps({'valid':success}))
                    
                except Institution.DoesNotExist:
                    raise Http404
                
            else:
                return HttpResponse(json.dumps({'valid':success}))
            
        except KeyError as e:
            return HttpResponse(json.dumps({'valid':success}))
    else:
        raise Http404

#PROFILE
def get_error_message(request):
    if request.is_ajax():
        error_name = request.GET['name']
        
        error = PageMessages.objects.get(name=error_name)
        
        return HttpResponse(json.dumps({"error_header": error.header, "error_message":error.message}))
    else: raise Http404

def update_profile(request):
    #TODO: REGEX!!! + ERRORS
    if request.is_ajax():
        output = {
            'error':False
        }
        user_update = ProfileUpdate(request)
        
        type = request.GET['type']
        
        if type == 'first_name':
            user = user_update.update_first_name()
            output['first_name'] = user.first_name
            return HttpResponse(json.dumps(output))
        elif type == 'last_name':
            user = user_update.update_last_name()
            output['last_name'] = user.last_name
            return HttpResponse(json.dumps(output))
        
        elif type == 'education_delete':
            try:
                user_update.delete_education()
                return HttpResponse(json.dumps({"error":False}))
            except ClassDoesNotExists as e:
                return HttpResponse(json.dumps({"error":True, "error_header":e.header, "error_message":\
                    e.message}))
        
        elif type == 'previous_education':
            try:
                c = user_update.try_new_previous_education()
                return HttpResponse(json.dumps({'error':False}))
            except InvalidSchoolYears as e:
                return HttpResponse(json.dumps({"error":True, \
                    "error_header":e.header, "error_message":e.message}))
            except NotPreviousEducation as e:
                return HttpResponse(json.dumps({"error":True, \
                    "error_header":e.header, "error_message":e.message}))
                
        elif type == 'current_education':
            try:
                user = user_update.try_new_current_education()
                return HttpResponse(json.dumps({'error':False}))
            except NoCurrentSchoolError as e:
                return HttpResponse(json.dumps({"error":True, \
                    "error_header":e.header, "error_message":e.message}))
            except InvalidSchoolYears as e:
                return HttpResponse(json.dumps({"error":True, \
                    "error_header":e.header, "error_message":e.message}))
            
    else:
        raise Http404
    
def email_change_confirmation(request):
    if request.is_ajax():
        user = User.objects.get(pk=request.session['last_logged_user'])
        confirmation_code = request.GET['confirmation_code']
        
        user_confirmation_code = EmailChange.objects.filter(user=user).latest('change_time').change_code        
        
        if confirmation_code == user_confirmation_code:
            output = {'error': False}
            
            user.person.block_code = 0
            user.person.save()
            user.is_active = True
            user.save()
            
        else:
            output = {'error': True, 'error_header':'Wrong confirmation code', 'error_message':'The code you have provided is wrong!'}
            
        return HttpResponse(json.dumps(output))
    else:
        raise Http404


def add_to_watchlist(request):
    if request.is_ajax():
        watchlist = False
        
        b = Book.objects.get(pk=request.GET['book_id'])
        
        if request.GET['change'] == "false":
            try:
                w = WatchList.objects.get(user=request.user, book=b)
                watchlist = True
            except WatchList.DoesNotExist:
                watchlist = False
        else:
            try:
                w = WatchList.objects.get(user=request.user, book=b)
                w.delete()
                watchlist = False
            except WatchList.DoesNotExist:
                w = WatchList(user=request.user, book=b, added=datetime.datetime.now())
                w.save()
                watchlist = True
            
        return HttpResponse(json.dumps({'watchlist':watchlist}))
    else:
        raise Http404

@login_required
def list_books(request):
    if request.is_ajax():
        user = request.user
        books = Book.objects.filter(user=user).annotate(highest_offer=Max('offer'))

        load_type = request.POST.get('type', None)

        sections = []

        if load_type == 'books':
            """loading books sorted via: sold, offer made, no offers"""

            #geting all the objects which are made an offer but not sold
            offered_books = filter(lambda x: not x.is_sold(), books.filter(~Q(highest_offer=None)))

            if len(offered_books) != 0:
                output = {
                    'book_set': offered_books[:5],
                    'load_more':len(offered_books) > 5,
                    'section_name': 'Books with offers',
                    'section_id':'books_offers'
                }

                sections.append(output)

            #all books which are not sold and havent had an offer yet
            my_books = filter(lambda x: not x.is_sold(), books.filter(highest_offer=None))

            if len(my_books) != 0:
                output = {
                    'book_set':my_books[:5],
                    'load_more': len(my_books) > 5,
                    'section_name':'Other Books',
                    'section_id':'books_other'
                }

                sections.append(output)

        elif load_type == 'sold':
            in_operation = filter(lambda x: not x.is_finalised() and x.is_sold(), books)

            if len(in_operation) != 0:
                output = {
                    'book_set':in_operation[:5],
                    'load_more':len(in_operation) >5,
                    'section_id':'ongoing_selling',
                    'section_name':'Ongoing'
                }

                sections.append(output)

            finalised = filter(lambda x: x.is_finalised() and x.is_sold(), books)

            if len(finalised) != 0:

                output = {
                    'book_set':finalised[:5],
                    'load_more':len(finalised) > 5,
                    'section_id':'finalised_selling',
                    'section_name':'Finalised'
                }

                sections.append(output)
        elif load_type == 'bought':
            #load the books where sold_to = user
            books = Book.objects.filter(sold_to=user)

            in_operation = filter(lambda x: not x.is_finalised(), books)

            if len(in_operation) != 0:
                output = {
                    'book_set':in_operation[:5],
                    'load_more':len(in_operation) > 5,
                    'section_id':'ongoing_buying',
                    'section_name':'Ongoing'
                }

                sections.append(output)

            finalised = filter(lambda x: x.is_finalised(), books)

            if len(finalised) != 0:
                output = {
                    'book_set':finalised[:5],
                    'load_more':len(in_operation) >5,
                    'section_id':'finalised_buying',
                    'section_name':'Finalised'
                }
                sections.append(output)

        elif load_type == 'watchlist':
            w = WatchList.objects.filter(user=user)
            watched_books = map(lambda x: x.book, w)

            if len(watched_books) != 0:
                output = {
                    'book_set':watched_books[:5],
                    'load_more': len(watched_books) > 5,
                    'section_id': 'watchlist'
                }

                sections = [output]

        elif load_type == 'offers':
            """books which I made offer for, and are not sent to me"""
            offers = Offer.objects.filter(made_by=user).order_by('-made_time').filter(~Q(book__sold_to=user))

            #getting the books from offers
            books_offered = map(lambda x: x.book, offers)

            #making the books_offered distinct
            books_offered = list(set(books_offered))

            if len(books_offered) != 0:
                output = {
                    'book_set':books_offered[:5],
                    'load_more': len(books_offered) > 5,
                    'section_id':'my_offers'
                }

                sections = [output]
        else:
            raise Http404
        
        return render(request, 'after_login/books/list_books_page.html', {'sections': sections})
    else:
        raise Http404

@login_required
def load_all_books(request):
    
    if request.is_ajax():
        user = request.user
        books = Book.objects.filter(user=user).annotate(highest_offer=Max('offer'))

        section = request.POST.get('section', None)

        #TODO: check if length is more than 5

        if section == 'books_offers':
            books = filter(lambda x: not x.is_sold(), books.filter(~Q(highest_offer=None)))[5:]

        elif section == 'books_other':
            books = filter(lambda x: not x.is_sold(), books.filter(highest_offer=None))[5:]

        elif section == 'books_sold':
            books = filter(lambda x: x.is_sold(), books)[5:]

        elif section == 'watchlist':
            w = WatchList.objects.filter(user=user)
            books = map(lambda x: x.book, w)[5:]

        elif section == 'my_offers':
            offers = Offer.objects.filter(made_by=user).order_by('-made_time')
            #getting the books from offers
            books = map(lambda x: x.book, offers)

            #making the books_offered distinct
            books = list(set(books_offered))[5:]

        elif section == 'ongoing_selling':
            books = filter(lambda x: not x.is_finalised(), books)

        elif section == 'finalised_selling':
            books = filter(lambda x: x.is_finalised(), books)

        elif section == 'ongoing_buying':
            books = Book.objects.filter(sold_to=user)

            books = filter(lambda x: not x.is_finalised(), books)

        elif section == 'finalised_buying':
            books = Book.objects.filter(sold_to=user)

            books = filter(lambda x: x.is_finalised(), books)

        else:
            raise Http404

        return render(request, 'after_login/books/list_books_page.html', {'books':books})

    else:
        raise Http404
    
def check_username_available(request):
    if request.is_ajax():
        username = request.GET['user-username']
        output = {'valid':True}
        
        try:
            User.objects.get(username=username)
            output['valid'] = False
        except User.DoesNotExist:
            pass
            
        
        return HttpResponse(json.dumps(output))
    else:
        raise Http404
    
def load_conversation(request):
    if request.is_ajax():
        user = request.user
        
        try:
            t_id = request.POST['transaction_id']
        except KeyError:
            raise Http404
        
        t = get_object_or_404(Transaction, pk = t_id)
        
        if t.book.user.id == user.id or t.book.sold_to.id == user.id:
            messages = Message.objects.filter(transaction=t).order_by('send_date')
            
            #make all messages of the conversation seen
            
            unseen = messages.filter(seen=False).exclude(sender=request.user)
            
            for m in unseen:
                m.seen = True
                m.save()
            
            return render(request,
                          'after_login/user_messages/earlier_messages.html',
                          {'messages':messages})
            
        else:
            raise Http404 #TODO: content not visible for other users
        
    else:
        raise Http404

@login_required
def rate_transaction(request):
    if request.is_ajax() and request.method == 'POST':
        tr_id = request.POST.get('tr_id', None)
        rating = request.POST.get('rating', None)
        user = request.user

        if tr_id is None or rating is None:
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

            return HttpResponse(json.dumps({'success': True}))

        except TransactionRating.DoesNotExist:
            raise Http404

    else:
        raise Http404


@login_required
def delete_notification(request):
    if request.POST['pk'] is None:
        raise Http404
    else:
        notification = get_object_or_404(Notification, pk=request.POST['pk'])
        if notification.recipient.pk == request.user.pk:
            notification.deleted = True
            notification.save()

            return HttpResponse(json.dumps({'success': True}))
        else:
            raise Http404


@login_required
def mark_notification_read(request):
    if request.POST['pk'] is None:
        raise Http404
    else:
        notification = get_object_or_404(Notification, pk=request.POST['pk'])
        if notification.recipient.pk == request.user.pk:
            notification.mark_as_read()
            notification.save()

            return HttpResponse(json.dumps({'success': True}))
        else:
            raise Http404
