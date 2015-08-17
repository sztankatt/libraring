from django.dispatch import Signal, receiver
from django.contrib.auth.models import User
from books.models import Book, Offer
from django.utils.translation import ugettext_lazy as _
from notifications import notify

book_new_offer = Signal()
new_highest_offer = Signal(
    providing_args=['receiver', 'previous_offer', 'book'])
interesting_book_uploaded = Signal(providing_args=['user_list'])
book_finalised_by_other_user = Signal(providing_args=['book'])
new_message = Signal(providing_args=['receiver', 'book'])


@receiver(book_new_offer, sender=Offer)
def book_new_offer_receiver(sender, **kwargs):
    offer = kwargs['offer']
    notify.send(
        offer.made_by,
        recipient=offer.book.user,
        verb=_('made a new offer for'),
        target=offer.book,
        action_object=offer,
        description=_(
            """This book has a new offer of &pound;%(price)s. made by %(user)s.
            In case it is suitable for you, do not hesitate, go ahead
            and accept it!"""
            % {'price': offer.offered_price, 'user': offer.made_by.username}))


@receiver(new_highest_offer, sender=User)
def new_highest_offer_receiver(sender, **kwargs):
     kwargs['receiver']


@receiver(interesting_book_uploaded, sender=Book)
def interesting_book_uploaded_receiver(sender, **kwargs):
    return kwargs['user_list']


@receiver(book_finalised_by_other_user, sender=User)
def book_finalised_by_other_user_receiver(sender, **kwargs):
    return kwargs['book']


@receiver(new_message, sender=User)
def new_message_receiver(sender=User, **kwargs):
    return kwargs['receiver']
