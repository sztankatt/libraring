from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Max
from django.template.loader import get_template
from django.template import Context

from user_messages.models import Message
from user_messages.forms import MessageForm

from usr.project import user_is_not_blocked

from books.models import Book, Transaction

import datetime

from drealtime import iShoutClient
ishout_client = iShoutClient()

# Create your views here.

@login_required
@user_is_not_blocked
def main(request):
    sold_books = Transaction.objects.filter(book__user=request.user).annotate(last_sent=Max('message__send_date')).order_by('-last_sent')
    bought_books = Transaction.objects.filter(book__sold_to=request.user).annotate(last_sent=Max('message__send_date')).order_by('-last_sent')
    
    return render(request, 'after_login/user_messages/messages_main.html', {'buying_c_list':bought_books, 'selling_c_list':sold_books})

@login_required
@user_is_not_blocked
def conversation(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)

    #checking if the user has permission

    if request.user == transaction.book.user:
        selling = True
    elif request.user == transaction.book.sold_to:
        selling = False
    else:
        raise Http404

    if transaction.finalised_by_seller and transaction.finalised_by_buyer:
        return HttpResponseRedirect(reverse('user_messages:transaction_rate', args=(transaction.id, )))
    
    form = MessageForm({
        'sender' : request.user.id,
        'transaction':transaction.id
    })
    
    sold_books = Transaction.objects.filter(book__user=request.user).annotate(last_sent=Max('message__send_date')).order_by('-last_sent')
    bought_books = Transaction.objects.filter(book__sold_to=request.user).annotate(last_sent=Max('message__send_date')).order_by('-last_sent')
    
    return render(request, 'after_login/user_messages/conversation.html',
                  {
                    'form': form,
                    'transaction':transaction,
                    'selling':selling,
                    'buying_c_list':bought_books, 'selling_c_list':sold_books
                    })

@login_required
def add_new_message(request):
    if request.is_ajax() and request.method == 'POST':
        form = MessageForm(request.POST)

        #form is valid, we save the message and return it to both users
        if form.is_valid():
            message = form.save(commit=False)
            message.send_date = datetime.datetime.now()

            message.save()

            template = get_template('after_login/user_messages/earlier_messages.html')

            context = Context({'messages':[message]})

            output = template.render(context)

            #working out the receiver's ID
            transaction = message.transaction

            sender_id = message.sender.id

            if transaction.book.user.id == sender_id:
                receiver_id = transaction.book.sold_to.id
            elif transaction.book.sold_to.id == sender_id:
                receiver_id = transaction.book.user.id

            ishout_client.emit(
               int(receiver_id),
                'messages',
                data = {'msg':output, 'transaction_id':transaction.id}
            )
                

            return HttpResponse(output)

        else:
            return HttpResponse('the form is invalid')
    else:
        raise Http404