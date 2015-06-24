import datetime
import string
import random

from mysite.settings import DEBUG
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.template import Context
from django.core import mail
from django.template.loader import get_template

from usr.models import Class, Institution, Course, PageMessages, EmailChange, Person

#from user_messages.models import Conversation

PROJECT_NAME = 'Libraring'
PROJECT_CREATOR = 'Tamas Sztanka-Toth'
LAST_MODIFIED_DATE = '05/05/2014'

PROJECT_URL = 'www.libraring.co.uk'

REGISTRATION_EMAIL = PROJECT_NAME + '@no-reply.co.uk'


def project_info(request):
    #calculating the number of new messages
    
 #    num = 0
    
 #    user = request.user
    
 #    if user.is_authenticated():
	# s_conv = Conversation.objects.filter(selling_user=user)
	
	# b_conv = Conversation.objects.filter(buying_user=user)
	
	# for c in s_conv:
	#     if c.new_selling_messages():
	# 	num = num + 1
	
	# for c in b_conv:
	#     if c.new_buying_messages():
	# 	num = num + 1
	
    return {
		'project':{
		    'name': PROJECT_NAME,
		    'debug':DEBUG,
		},
	#'msg':{
	    #'new_number':num
	#}
    }

"""decorators"""
def user_is_not_blocked(original_function):
    def block_check(request, *args, **kwargs):
	if request.user.is_active == True:
	    return original_function(request, *args, **kwargs)
	else:
	    user = request.user
	    logout(request)
	    request.session['last_logged_user'] = user.id
	    return HttpResponseRedirect(reverse('usr:blocked_profile'))
    
    return block_check

def last_logged_user_exists(original_function):
    def block_check(request, *args, **kwargs):
	try:
	    user_id = request.session['last_logged_user']
	    return original_function(request, *args, **kwargs)
	except KeyError as e:
	    return HttpResponseRedirect(reverse('usr:login'))
    
    return block_check
	
def user_not_authenticated(original_function):
    def block_check(request, *args, **kwargs):
	if request.user.is_authenticated():
	    return HttpResponseRedirect(reverse('index'))
	else:
	    return original_function(request, *args, **kwargs)
	
    return block_check


"""helper functions"""


#helper functions for generating confirmation code for the user
def generate_random(size=50, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

#confirmation code generator. Checks whether the given code already exists, if yes, generates a
#new one
def confirmation_code_generator():
	code = generate_random()
	while Person.objects.filter(confirmation_code=code).exists():
		code = generate_random()
		
	return code

def generate_email_change_code():
    code = generate_random(size=6, chars=string.ascii_uppercase + string.digits)
    return code

def send_new_email_code(email_change):
    sender = 'LIBRARING <no-reply@libraring.co.uk>'
    to = email_change.email_to
    subject = 'Email change code'
    
    text_content = get_template('before_login/registration/change_code_email.txt')
    html_content = get_template('before_login/registration/change_code_email.html')
    
    d = Context({'email_change':email_change})
    
    text_content = text_content.render(d)
    html_content = html_content.render(d)
    
    
    m = mail.EmailMultiAlternatives(subject, text_content, sender, [to])
    m.attach_alternative(html_content, 'text/html')
    m.send()


"""helper classes"""

class NoCurrentSchoolError(Exception):
    def __init__(self):
	p = PageMessages.objects.get(name='no_current_education')
        self.header = p.header
	self.message = p.message
	
class NotPreviousEducation(Exception):
    def __init__(self):
	p = PageMessages.objects.get(name='not_previous_education')
        self.header = p.header
	self.message = p.message

class InvalidSchoolYears(Exception):
    def __init__(self):
	p = PageMessages.objects.get(name='invalid_school_years')
        self.header = p.header
	self.message = p.message
	
class ClassDoesNotExists(Exception):
    def __init__(self):
	p = PageMessages.objects.get(name='class_does_not_exist')
	self.header = p.header
	self.message = p.message
	
class WrongEmailEnding(Exception):
    def __init__(self):
	p = PageMessages.objects.get(name='wrong_email_ending')
	self.header = p.header
	self.message = p.message

class ProfileUpdate():
    def __init__(self, request):
	self.request = request
	self.user = request.user

    def update_first_name(self):
	self.user.first_name = self.request.GET['first_name']
	self.user.save()
	return self.user
    
    def update_last_name(self):
	self.user.last_name = self.request.GET['last_name']
	self.user.save()
	return self.user
    
    def try_new_current_education(self):
    	data = self.request.GET
	c_end_year = self.user.person.current_education().end_year
	if c_end_year > int(data['end_year']):
	    raise NoCurrentSchoolError()
	elif int(data['end_year']) < int(data['start_year']):
	    raise InvalidSchoolYears()
	
	return True
    
    def update_current_education(self):
	data = self.request.POST
	c_end_year = self.user.person.current_education().end_year
	if c_end_year > int(data['end_year']):
	    raise NoCurrentSchoolError()
	elif int(data['end_year']) < int(data['start_year']):
	    raise InvalidSchoolYears()
	else:
	    new_institution = Institution.objects.get(pk=data['institution'])
	    new_course = Course.objects.get(pk=data['course'])
	    obj, created = Class.objects.get_or_create(
		institution=new_institution, 
		course=new_course,
		start_year=data['start_year'], 
		end_year=data['end_year'])
	    self.user.person.education.add(obj)
	    self.user.person.block_code = 2
	    
	    
	    #changing the email
	    new_email = data['email']
	    
	    #check if the email ending is correct
	    if not new_email.endswith(self.user.person.new_institution.email_ending):
		raise WrongEmailEnding()
	    
	    self.user.person.save()
	    
	    new_email = data['email'] 	    
	    old_email = self.user.email
	    
	    self.user.email = new_email
	    self.user.is_active = False
	    self.user.save()
	    
	    #saving the change
	    m = EmailChange(user=self.user, email_from = old_email, email_to = new_email, change_time = datetime.datetime.now(),\
		change_code=generate_email_change_code())
	    m.save()
	    
	    send_new_email_code(m)
	    
	    return self.user
    
    def try_new_previous_education(self):
	data = self.request.GET
		
	if int(data['start_year']) > int(data['end_year']):
	    raise InvalidSchoolYears()
	
	if int(data['end_year']) > self.user.person.current_education().end_year:
	    raise NotPreviousEducation()
	
	return True
    
    def add_new_education(self):
	data = self.request.POST
	new_institution = Institution.objects.get(pk=data['institution'])
	new_course = Course.objects.get(pk=data['course'])
	obj, created = Class.objects.get_or_create(
	    institution=new_institution, 
	    course=new_course,
	    start_year=data['start_year'], 
	    end_year=data['end_year'])
	
	if data['start_year'] > data['end_year']:
	    raise InvalidSchoolYears()
	
	if int(obj.end_year) > self.user.person.current_education().end_year:
	    raise NotPreviousEducation()
	
	self.user.person.education.add(obj)
	self.user.person.save()
	self.user.save()
	
	return obj
    
    def delete_education(self):
	education_id = self.request.GET['education_id']
	try:
	    education = Class.objects.get(pk=education_id)
	except Class.DoesNotExists as e:
	    raise ClassDoesNotExists()
	
	self.user.person.education.remove(education)
	self.user.person.save()
	self.user.save()
	
	return self.user
