from django.dispatch import Signal, receiver
from django.contrib.auth.models import User
from books.models import Book, Offer, Transaction
from django.utils.translation import ugettext_lazy as _
from notifications import notify
from mailer import send_html_mail
from django.template.loader import get_template
from django.template import Context

book_new_offer = Signal()
new_highest_offer = Signal(
    providing_args=['offer', 'user', 'previous_user',
                    'previous_offer', 'book'])
interesting_book_uploaded = Signal(providing_args=['user_list', 'book'])
book_finalised_by_other_user = Signal(
    providing_args=['transaction', 'finalised_by_seller', 'buyer', 'seller'])
new_message = Signal(providing_args=['receiver', 'book'])
accepted_offer = Signal(providing_args=['seller', 'buyer', 'book'])


def send_notification_mail(
        sent_from, verb, subject, body, recipient, target,
        sender_address='LIBRARING <no-reply@libraring.co.uk>'):
    sender = sender_address
    to = recipient.email
    subject = subject
    text_content = get_template('after_login/usr/notification_email.txt')
    html_content = get_template('after_login/usr/notification_email.html')

    d = Context({'body': body, 'user': recipient, 'verb': verb,
                'target': target, 'sent_from': sent_from})

    text_content = text_content.render(d)
    html_content = html_content.render(d)

    send_html_mail(subject, text_content, html_content, sender, [to])


@receiver(book_new_offer, sender=Offer)
def book_new_offer_receiver(sender, **kwargs):
    offer = kwargs['offer']
    recipient = offer.book.user
    body = _(
                """This book has a new offer of &pound;%(price)s. made by %(user)s.
                In case it is suitable for you, do not hesitate, go ahead
                and accept it!"""
                % {
                    'price': offer.offered_price,
                    'user': offer.made_by.username})
    subject = _('New offer for %(book)s' % {'book': offer.book})
    target = offer.book
    verb = _('has made a new offer for your book: ')
    if recipient.app_notifications.my_book_new_offer:
        notify.send(
            offer.made_by,
            recipient=recipient,
            verb=verb,
            target=target,
            action_object=offer,
            description=body)

    if recipient.email_notifications.my_book_new_offer:
        send_notification_mail(
            offer.made_by, verb, subject, body, recipient, target)


@receiver(new_highest_offer, sender=User)
def new_highest_offer_receiver(sender, **kwargs):
    previous_user = kwargs['previous_user']
    previous_price = kwargs['previous_highest']
    book = kwargs['book']
    target = book
    recipient = kwargs['user']
    offer = kwargs['offer']
    body = _(
                """%(user)s has offered a higher price for %(book)s (&pund; %(price)s)
                than you did %(previous_price)s.
                If you do not want to loose this opportunity,
                increase your offer!"""
                % {
                    'user': recipient,
                    'book': book,
                    'price': offer.offered_price,
                    'previous_price': previous_price})
    subject = _("""%(user)s has the new highest offer for %(book)s""" % {
            'user': previous_user, 'book': book
        })
    verb = _('has the new highest offer for')
    if recipient.app_notifications.other_user_highest_offer:
        notify.send(
            previous_user,
            recipient=recipient,
            verb=verb,
            target=target,
            action_object=offer,
            description=body)

    if recipient.email_notifications.other_user_highest_offer:
        send_notification_mail(
            previous_user, verb, subject, body, recipient, target)


@receiver(interesting_book_uploaded, sender=Book)
def interesting_book_uploaded_receiver(sender, **kwargs):
    user_list = kwargs['user_list']
    book = kwargs['book']
    target = book
    verb = _('uploaded a new book which might interest you:')
    subject = _(
        """%(user)s has uploaded a book that might interest you"""
        % {'user': book.user})
    for user in user_list:
        body = _(
            """%(user)s has uploaded a new book, entilted %(book)s with goal
            price of %(price)s which might interest you. Do not hesitate
            and make an offer!"""
            % {'user': user, 'book': book, 'price': book.price})
        if user.app_notifications.interesting_book_uploaded:
            notify.send(
                book.user,
                recipient=user,
                verb=verb,
                target=book,
                description=body)

        if user.email_notifications.interesting_book_uploaded:
            send_notification_mail(
                book.user, verb, subject, body, user, target)


@receiver(book_finalised_by_other_user, sender=User)
def book_finalised_by_other_user_receiver(sender, **kwargs):
    transaction = kwargs['transaction']
    buyer = kwargs['buyer']
    seller = kwargs['seller']
    finalised_by_seller = kwargs['finalised_by_seller']
    target = transaction.offer.book
    verb = _('has finalised the transaction for ')
    subject = _('Transaction finalised for %(book)s' % {'book': target})
    body_text = """%(user)s has finalised the transaction for
        %(book)s. If you think this transaction is finalised,
        go ahaed and finalise it as well!
        """
    if finalised_by_seller:
        user = seller
        recipient = buyer
    else:
        user = buyer
        recipient = seller

    body = _(body_text % {'user': user, 'book': target})
    if recipient.app_notifications.book_finalised_by_other_user:
        notify.send(
            user,
            recipient=recipient,
            verb=verb,
            target=target,
            description=body)
    if recipient.email_notifications.book_finalised_by_other_user:
        send_notification_mail(
            user, verb, subject, body, recipient, target)


@receiver(book_finalised_by_other_user, sender=Transaction)
def book_transfer_finalised(sender, **kwargs):
    transaction = kwargs['transaction']
    buyer = kwargs['buyer']
    seller = kwargs['seller']
    target = transaction.offer.book
    verb = _('has been closed for ')
    subject = _('Transaction has been closed for %(book)s' % {'book': target})
    body = _(
        """The transaction for %(book)s has been closed. Please rate
        the transaction on the book's page.
        """ % {'book': target})

    if seller.app_notifications.book_finalised_by_other_user:
        notify.send(
            transaction,
            recipient=seller,
            verb=verb,
            target=target,
            description=body)

    if seller.email_notifications.book_finalised_by_other_user:
        send_notification_mail(
            transaction, verb, subject, body, seller, target)

    if buyer.app_notifications.book_finalised_by_other_user:
        notify.send(
            transaction,
            recipient=buyer,
            verb=verb,
            target=target,
            description=body)

    if buyer.email_notifications.book_finalised_by_other_user:
        send_notification_mail(
            transaction, verb, subject, body, buyer, target)


@receiver(accepted_offer, sender=User)
def accepted_offer_receiver(sender=User, **kwargs):
    seller = kwargs['seller']
    buyer = kwargs['buyer']
    target = kwargs['book']
    verb = _('has accepted your offer for')
    subject = _('Offer for %(book)s has been accepted' % {'book': target})
    email_body = _(
        """Your offer of &pound;%(price)s for %(book)s has been accepted!
        To further discuss the details of this transaction, please reply to
        this email, or write one to %(user)s at %(email)s.
        """ % {
                'price': target.accepted_offer().offered_price,
                'book': target,
                'user': target.user,
                'email': target.user.email})

    body = _(
        """Your offer of &pound;%(price)s for %(book)s has been accepted!
        To further discuss the details of this transaction, please write
        an emai to %(user)s at %(email)s
        """ % {
                'price': target.accepted_offer().offered_price,
                'book': target,
                'user': target.user,
                'email': target.user.email})

    if buyer.app_notifications.accepted_offer:
        notify.send(
            seller,
            recipient=buyer,
            verb=verb,
            target=target,
            description=body)

    if buyer.email_notifications.accepted_offer:
        send_notification_mail(
            seller, verb, subject, email_body, buyer, target,
            sender_address=seller.username+'<'+seller.email+'>')


@receiver(new_message, sender=User)
def new_message_receiver(sender=User, **kwargs):
    return kwargs['receiver']
