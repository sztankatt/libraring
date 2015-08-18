from django.dispatch import Signal, receiver
from django.contrib.auth.models import User
from books.models import Book, Offer
from django.utils.translation import ugettext_lazy as _
from notifications import notify

book_new_offer = Signal()
new_highest_offer = Signal(
    providing_args=['offer', 'user', 'previous_user', 'previous_offer', 'book'])
interesting_book_uploaded = Signal(providing_args=['user_list', 'book'])
book_finalised_by_other_user = Signal(providing_args=['book'])
new_message = Signal(providing_args=['receiver', 'book'])


@receiver(book_new_offer, sender=Offer)
def book_new_offer_receiver(sender, **kwargs):
    offer = kwargs['offer']
    notify.send(
        offer.made_by,
        recipient=offer.book.user,
        verb=_('has made a new offer for your book: '),
        target=offer.book,
        action_object=offer,
        description=_(
            """This book has a new offer of &pound;%(price)s. made by %(user)s.
            In case it is suitable for you, do not hesitate, go ahead
            and accept it!"""
            % {'price': offer.offered_price, 'user': offer.made_by.username}))


@receiver(new_highest_offer, sender=User)
def new_highest_offer_receiver(sender, **kwargs):
    previous_user = kwargs['previous_user']
    previous_offer = kwargs['previous_higher']
    book = kwargs['book']
    user = kwargs['user']
    offer = kwargs['offer']
    notify.send(
        previous_user,
        recipient=user,
        verb=_('has the new highest offer for'),
        target=book,
        action_object=offer,
        description=_(
            """%(user)s has offered a higher price for %(book)s (&pund; %(price)s)
            than you did %(previous_price)s.
            If you do not want to loose this opportunity,
            increase your offer!"""
            % {
                'user': user,
                'book': book,
                'price': offer.offered_price,
                'previous_offer': previous_offer}))


@receiver(interesting_book_uploaded, sender=Book)
def interesting_book_uploaded_receiver(sender, **kwargs):
    user_list = kwargs['user_list']
    book = kwargs['book']

    for user in user_list:
        notify.send(
            book.user,
            recipient=user,
            verb=_('uploaded a new book which might interest you:'),
            target=book,
            description=_(
                """%(user)s has uploaded a new book, entilted %(book)s with goal
                price of %(price)s which might interest you. Do not hesitate
                and make an offer!"""
                % {'user': user, 'book': book, 'price': book.price}))


@receiver(book_finalised_by_other_user, sender=User)
def book_finalised_by_other_user_receiver(sender, **kwargs):
    return kwargs['book']


@receiver(new_message, sender=User)
def new_message_receiver(sender=User, **kwargs):
    return kwargs['receiver']
