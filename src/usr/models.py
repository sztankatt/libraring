import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from books.models import Transaction

COUNTRIES = [
    ('UK', 'United Kingdom'),
    ('HU', 'Hungary'),
]

alphanumeric_regex = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

#location model for Institution
class Location(models.Model):

    country 			= models.CharField(choices=COUNTRIES, max_length=2)
    postcode			= models.CharField(max_length=10, null=True, validators=[alphanumeric_regex])
    city				= models.CharField(max_length=50)
    #county              = models.CharField(blank=True, null=True, max_length=50)

    # def __unicode__(self):
    #     if self.country == '--None--':
    #         return '%s, %s' % (self.city, self.country)
    #     else:
    #         return '%s, %s, %s' % (self.city, self.county, self.country)

#Institution for Person, Classes
class Institution(models.Model):
    name 				= models.CharField(max_length=200, unique=True)
    location 			= models.ForeignKey(Location)
    email_ending		= models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name

class Course(models.Model):
    name 	= models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return self.name

class Class(models.Model):
    institution	 		= models.ForeignKey(Institution)
    course 				= models.ForeignKey(Course)
    start_year 			= models.IntegerField(max_length=4, choices=[(x, x) for x in range (1950, datetime.datetime.now().year+1)])
    end_year			= models.IntegerField(max_length=4, choices=[(x, x) for x in range (1950, datetime.datetime.now().year+10)])

    def __unicode__(self):
        return '%s-%s, %s, %s' % (self.start_year, self.end_year, self.course.name, self.institution.name)


#the model of Person
class Person(models.Model):
    STUDENT = 'S'
    TEACHER = 'T'
    LECTURER = 'L'

    PERSON_TYPE_CHOICES = (
        (STUDENT, 'Student'),
        (TEACHER, 'Teacher'),
        (LECTURER, 'University Lecturer'),
    )

    PERSON_TITLE_CHOICES = (
        ('MR', 'Mr.'),
        ('MRS', 'Mrs.'),
        ('MS', 'Ms.'),
        ('MSS', 'Miss.'),
        ('DR', 'Dr.'),
        ('PRF', 'Prof.'),
    )

    user        		= models.OneToOneField(User, primary_key=True)
    title			    = models.CharField(max_length=3, choices=PERSON_TITLE_CHOICES)
    date_born   		= models.DateField('date born', blank=True, null=True)
    about       		= models.TextField(blank=True)
    education   		= models.ManyToManyField(Class, blank=True, related_name='students')
    person_type 		= models.CharField(max_length=1, choices=PERSON_TYPE_CHOICES, default=STUDENT)
    institution		    = models.ForeignKey(Institution, blank=True, null=True)
    confirmation_code	= models.CharField(max_length=50, unique=True)
    block_code		    = models.IntegerField(default=1, blank=True)
    #location            = models.ForeignKey(Location)

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
        return self.education.filter(end_year__lt=self.education.order_by('-end_year')[0].end_year).order_by('-end_year')

    # def location(self):
    # 	if self.institution is None:
    # 		return self.current_education().institution.location.__unicode__()
    # 	else:
    # 		return self.institution.location.__unicode__()


    def __unicode__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)

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