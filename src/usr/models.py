import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _
from location_field.models.plain import PlainLocationField
from books.models import TransactionRating

COUNTRIES = [
    ('UK', 'United Kingdom'),
    ('HU', 'Hungary'),
]

alphanumeric_regex = RegexValidator(
    r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')


class Institution(models.Model):
    name = models.CharField(max_length=200, unique=True)
    city = models.CharField(max_length=255)
    location = PlainLocationField(based_fields=[city], zoom=7)
    email_ending = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return self.name


class Class(models.Model):
    institution = models.ForeignKey(Institution)
    course = models.ForeignKey(Course)
    start_year = models.IntegerField(
        max_length=4,
        choices=[(x, x) for x in range(1950, datetime.datetime.now().year+1)])
    end_year = models.IntegerField(
        max_length=4,
        choices=[(x, x) for x in range(1950, datetime.datetime.now().year+10)])

    def __unicode__(self):
        return '%s-%s, %s, %s' % (
            self.start_year,
            self.end_year,
            self.course.name,
            self.institution.name)


class Person(models.Model):
    STUDENT = 'S'
    TEACHER = 'T'
    LECTURER = 'L'

    PERSON_TYPE_CHOICES = (
        (STUDENT, 'Student'),
        (TEACHER, 'Teacher'),
        (LECTURER, 'University Lecturer'),
    )

    user = models.OneToOneField(User, primary_key=True)
    date_born = models.DateField('date born', blank=True, null=True)
    education = models.ManyToManyField(
        Class, blank=True, related_name='students')
    person_type = models.CharField(
        max_length=1, choices=PERSON_TYPE_CHOICES, default=STUDENT)
    institution = models.ForeignKey(Institution, blank=True, null=True)
    confirmation_code = models.CharField(max_length=50, unique=True)
    block_code = models.IntegerField(default=1, blank=True)

    city = models.CharField(max_length=255)
    location = PlainLocationField(based_fields=[city], zoom=7)

    def is_student(self):
        if self.person_type == 'S':
            return True
        else:
            return False

    def current_education(self):
        if self.is_student():
            return self.education.order_by('-end_year')[0]
        else:
            return None

    def previous_education(self):
        return self.education.filter(
            end_year__lt=self.education.order_by('-end_year')[0]
            .end_year).order_by('-end_year')

    def get_average_rating(self):
        rating = None

        as_seller = TransactionRating.objects.filter(seller=self.user)
        as_buyer = TransactionRating.objects.filter(buyer=self.user)

        seller_count = as_seller.count()
        buyer_count = as_buyer.count()

        if seller_count != 0 and buyer_count != 0:
            rating_sum = float(
                as_seller.aggregate(Sum('seller_rating'))['seller_rating__sum']
            )
            rating_sum += float(
                as_buyer.aggregate(Sum('buyer_rating'))['buyer_rating__sum']
            )
            rating = rating_sum/(seller_count+buyer_count)
        elif seller_count == 0:
            rating = float(
                as_buyer.aggregate(Sum('buyer_rating'))['buyer_rating__sum']
            )
            rating /= buyer_count
        elif buyer_count == 0:
            rating = float(
                as_seller.aggregate(Sum('seller_rating'))['seller_rating__sum']
            )
            rating /= seller_count

        return rating

    def __unicode__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)


class NotificationMixin(models.Model):
    my_book_new_offer = models.BooleanField(
        default=True,
        verbose_name=_('One of my books has a new offer')
        )

    other_user_highest_offer = models.BooleanField(
        default=True,
        verbose_name=_('Someone offered a higher price for a book than me')
        )

    interesting_book_uploaded = models.BooleanField(
        default=True,
        verbose_name=_('A book that might be of my interest has been uploaded')
        )

    book_finalised_by_other_user = models.BooleanField(
        default=True,
        verbose_name=_(
            'A book that I have sold has been finalised by the buyer'
            )
        )

    accepted_offer = models.BooleanField(
        default=True,
        verbose_name=_(
            'One of your offers has been accepted'
            )
        )

    class Meta:
        abstract = True


class AppNotifications(NotificationMixin):
    user = models.OneToOneField(User, related_name='app_notifications', unique=True)


class EmailNotifications(NotificationMixin):
    user = models.OneToOneField(User, related_name='email_notifications', unique=True)
    new_message = models.BooleanField(
        default=True,
        verbose_name=_('I received a new message')
        )


class PageMessages(models.Model):
    ERROR_TYPES = (
        ('danger', 'danger'),
        ('warning', 'warning'),
        ('info', 'info'),
        ('success', 'success'),
    )
    type = models.CharField(max_length=10, choices=ERROR_TYPES)
    name = models.CharField(max_length=30)
    header = models.CharField(max_length=50)
    message = models.TextField()

    def __unicode__(self):
        return "%s" % (self.header)


class EmailChange(models.Model):
    user = models.ForeignKey(User)
    email_from = models.EmailField()
    email_to = models.EmailField()
    change_time = models.DateTimeField()
    change_code = models.CharField(max_length=6)
