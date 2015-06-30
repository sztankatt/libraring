from django.db import models

from django.contrib.auth.models import User

from django.db.models.sql.query import FieldError

from django_countries.fields import CountryField

from django.db.models import Max, Q, Count


import datetime 

#TODO:solve migrations problem


class Author(models.Model):
    name = models.CharField(max_length=250)
    
    def __unicode__(self):
        return '%s' % (self.name)
    
class Genre(models.Model):
    name = models.CharField(max_length=250)
    

    def __unicode__(self):
        return '%s' % (self.name)
    
class Publisher(models.Model):
    name = models.CharField(max_length=250)
    
    def __unicode__(self):
        return '%s' % (self.name)
    
    
class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)

class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.ManyToManyField(Author)
    genre = models.ManyToManyField(Genre)
    edition = models.IntegerField(choices=[(x,x) for x in range(1,31)])
    publisher = models.ForeignKey(Publisher, blank=True, null=True)
    publication_year = IntegerRangeField(help_text='YYYY', min_value=1000, max_value=datetime.date.today().year)
    publication_city = models.CharField(max_length=100, blank=True, null=True)
    publication_country = CountryField(null=True, blank=True)
    
    user = models.ForeignKey(User)
    price = IntegerRangeField(min_value=1, max_value=200, verbose_name='Goal price')
    includes_delivery_charges = models.BooleanField(default=False)
    upload_date = models.DateField()
    isbn = models.CharField(max_length=13, blank=True, null=True) #regexp here!!!
    image = models.ImageField(upload_to='books', default='books/no_image.png', blank=True)

    short_description = models.TextField(blank=True, default="")

    #is_sold = models.BooleanField(default=False)

    STATUS_OPTIONS = [
        ('normal', 'normal'),
        ('offered', 'offered'),
        ('selling', 'selling'),
        ('finalised', 'finalised')
    ]

    status = models.CharField(max_length=20, choices=STATUS_OPTIONS, default ='normal')

    sold_to = models.ForeignKey(User, related_name='bough_book', null=True, blank=True)

    def __unicode__(self):
        return '%s' % (self.title)

    def is_sold(self):
        accepted_offers = Offer.objects.filter(book=self).filter(accepted=True)
        if len(accepted_offers) == 0:
            return None

        return accepted_offers[0]

    def is_finalised(self):
        accepted_offer = self.is_sold()
        if accepted_offer is None:
            return False
        else:
            t = Transaction.objects.get(offer=accepted_offer)
            try:
                tr = TransactionRating.objects.get(transaction=t)
                return True
            except TransactionRating.DoesNotExist:
                return False

    def get_location(self):
        return self.user.person.location()
    
    def get_absolute_url(self):
        return '/books/book/%s/' % (self.id)

    def get_highest_offer(self):
        try:
            return Offer.objects.filter(book=self).order_by('-offered_price')[0]
        except IndexError:
            return None

    class Meta:
        ordering = ['-upload_date']



class TransactionRating(models.Model):
    seller = models.ForeignKey(User, related_name='seller_transaction_rating')
    buyer = models.ForeignKey(User, related_name='buyer_transaction_rating')

    RATING_CHOICES = [(x,x) for x in range(1,6)]

    seller_rating = models.IntegerField(blank=True, null=True, choices=RATING_CHOICES)

    buyer_rating = models.IntegerField(blank=True, null=True, choices=RATING_CHOICES)


class Transaction(models.Model):
    finalised_by_buyer = models.BooleanField(default=False)
    finalised_by_seller = models.BooleanField(default=False)

    rating = models.OneToOneField(TransactionRating, null=True)

    # def new_selling_messages(self):
    #     from user_messages.models import Message
    #     return Message.objects.filter(transaction=self,
    #         seen=False).exclude(sender=self.book.user).count() > 0
    #
    # def new_buying_messages(self):
    #     from user_messages.models import Message
    #     return Message.objects.filter(transaction=self,
    #         seen=False).exclude(sender=self.book.sold_to).count() > 0

    def is_finalised(self):
        return (self.finalised_by_seller and self.finalised_by_buyer)


class Offer(models.Model):
    book = models.ForeignKey(Book)
    offered_price = IntegerRangeField(min_value=1, max_value=200)
    made_by = models.ForeignKey(User)
    made_time = models.DateTimeField(auto_now=True)
    accepted = models.BooleanField(default=False)

    transaction = models.OneToOneField(Transaction, null=True)


class WatchList(models.Model):
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    added = models.DateTimeField()
