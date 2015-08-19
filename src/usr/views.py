# Libraring project usr/views.py file
# Created by: Tamas Sztanka-Toth

from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core import mail
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.db.models import Q
from django.utils.translation import ugettext as _

from usr.forms import RegisterPersonForm, ClassForm,NClassForm, UserCreationForm, LoginForm,AppNotificationsForm,EmailNotificationsForm
from usr.models import Class, Person, PageMessages, AppNotifications, EmailNotifications
from usr.project import user_is_not_blocked, ProfileUpdate, \
    confirmation_code_generator, last_logged_user_exists, user_not_authenticated
from books.models import Genre, Book
from books.forms import GenreForm, BookForm
from notifications.models import Notification

def test(request):
    return render_to_response('ajaxSubmit.html');

#Data and functions for RegisterWizardView
FORMS = [("user", UserCreationForm),
         ("person", RegisterPersonForm)  #("class",ClassForm)
]

TEMPLATES = {
    "user": "before_login/registration/user.html",
    "person": "before_login/registration/person.html",  #"class":"before_login/registration/class.html",
    #"institution":"before_login/registration/institution.html"
}

#returns true iff the checkbox is set to student
def is_student(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('person') or {'person_type': 'none'}
    return cleaned_data['person_type'] == 'S'


#return true iff the checkbox is not set to student
def is_not_student(wizard):
    return not is_student(wizard)


def send_confirmation_email(user):
    sender = 'LIBRARING <no-reply@libraring.co.uk>'
    to = user.email
    subject = _('Registration confirmation')

    text_content = get_template('before_login/registration/email.txt')
    html_content = get_template('before_login/registration/email.html')

    d = Context({'user': user})

    text_content = text_content.render(d)
    html_content = html_content.render(d)

    m = mail.EmailMultiAlternatives(subject, text_content, sender, [to])
    m.attach_alternative(html_content, 'text/html')
    m.send()


#register wizard, using the Django's wizardView implementation
class RegisterWizard(SessionWizardView):
    #TODO: debugi this section properly
    #condition_dict = {'class':is_student, 'institution':is_not_student}

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    #after the last form has been submitted, ie everything is correct
    def done(self, form_list, **kwargs):
        #fetching and saving the user from the data of the first form
        user = form_list[0].save(commit=False)


        #fetching the details of user from the second form
        #user.email = form_list[2].cleaned_data['email']
        user.first_name = form_list[1].cleaned_data['first_name']
        user.last_name = form_list[1].cleaned_data['last_name']
        user.is_active = False


        #fetching the user's person object
        person = form_list[1].save(commit=False)

        person_data = form_list[1].cleaned_data

        #managing the user's person object
        person.person_type = 'S'  #education_data = form_list[2].cleaned_data
        #obj, created = Class.objects.get_or_create(
        #	institution=education_data['institution'],
        #	course=education_data['course'],
        #	start_year=education_data['start_year'],
        #	end_year=education_data['end_year'])

        #institution = None

        email = person_data['email']

        #if not email.endswith(education_data['institution'].email_ending):
        #	pass #return error

        #saving user.email, according to which institution was selected
        user.email = email
        user.save()

        person.user = user
        #person.institution = institution
        person.date_born = form_list[1].cleaned_data['date_born']
        person.confirmation_code = confirmation_code_generator()
        person.block_code = 3
        person.save()

        #if obj is not None:
        #    person.education.add(obj)
        #person.save()

        send_confirmation_email(user)

        self.request.session['last_logged_user'] = user.id

        return HttpResponseRedirect(reverse('usr:register_confirmation'))


#managing user login. If there is a next parameter, sending the user to the next page.
#otherwise sending him to '/'
#/usr/login/
def login_view(request):
    data = {}
    username = password = ''
    user = None
    error = ''

    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST['username'], \
                                password=request.POST['password'])
            error = _('Your username/password is incorrect. Are you registered?')

    else:
        form = LoginForm()

    next = ""

    if request.GET:
        next = request.GET['next']

    #if the user exists
    if user is not None:
        if user.is_active == True:
            try:
                del request.session['last_logged_user']
            except KeyError:
                pass

            login(request, user)
            if next == "":
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponseRedirect(next)
        else:
            request.session['last_logged_user'] = user.id
            return HttpResponseRedirect(reverse('usr:blocked_profile'))

    return render(request, 'before_login/auth/login.html', \
                  {
                      'form': form,
                      'error': error
                  })


#loggin out the user.
#/usr/logout
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


#view which handles the loading of main page for logged in users. Only called within 'index' view
@user_is_not_blocked
def home(
        request,
        template='after_login/usr/home.html',
        home_books_template ='after_login/usr/load_books.html'
        ):
    list = request.GET.getlist('genres')
    first_page = request.GET.get('page-number', 1)
    first_page = int(first_page)*8
    books = Book.objects.all()
    status = Q(status='normal') | Q(status='offered')
    books = books.filter(status)
    books = books.filter(~Q(user=request.user))
    if list:
        filter = Q()
        for genre in list:
            filter = filter | Q(genre__name=genre)

        books = books.filter(filter).distinct()

    context = {
        'books': books,
        'home_books_template': home_books_template,
        'form':GenreForm(request.GET),
        'list':list,
        'first_page':first_page
    }
    if request.is_ajax():
        template = home_books_template

    return render_to_response(template, context, context_instance=RequestContext(request))
    #g = Genre.objects.annotate(book_num=Count('book')).order_by('-book_num').exclude(book_num=0)

    #return render(request, 'after_login/usr/home.html', {'books': books})


#view which handles the access to the '/'
def index(request):
    #checks if the user is logged-in
    if request.user.is_authenticated():
        return home(request)

    return render(request, 'before_login/framework/index.html', {'form': LoginForm()})


# view which loads the profile
@login_required
@user_is_not_blocked
def load_profile(request):
    # becomes true if the user is viewing his own profile
    account_settings = False

    # checking whether the id in the request was specified
    id = request.user.id
    account_settings = True

    # return  HttpResponse(id)

    # fetching the user object
    user = get_object_or_404(User, pk=id)

    # checking if the usser is viewging his/her own profile
    if id == request.user.id:
        account_settings = True

    # will be true if the user is a student
    student = False

    # checking if the user is a student
    if user.person.person_type == 'S':
        student = True

    # passing fields for the profile
    fields = [
        {
            'label': 'Username',
            'data': user.username,
            'update': False,
        },
        {
            'label': 'First Name',
            'data': user.first_name,
            'update': True,
            'update_id': 'first_name',
            'form_id': 'first_name_form',
        },
        {
            'label': 'Last Name',
            'data': user.last_name,
            'update': True,
            'update_id': 'last_name',
            'form_id': 'last_name_form',
        },
        {
            'label'	: 'e-mail',
            'data'	: user.email,
            'update'	: False,
        }]

    app_notifications, created = AppNotifications.objects.get_or_create(user=request.user)
    email_notifications, created = EmailNotifications.objects.get_or_create(user=request.user)

    return render(request, 'after_login/usr/profile.html', {
        'user': user,
        'fields': fields,
        'settings': account_settings,
        'student': student,
        'app_notifications_form': AppNotificationsForm(instance=app_notifications),
        'email_notifications_form': EmailNotificationsForm(instance=email_notifications),
        'new_previous_education_form': NClassForm(
            auto_id='new_previous_education_%s')
        })


#not used anymore
@login_required
def change_current_education(request):
    p_u = ProfileUpdate(request)

    #try:	
    user = p_u.update_current_education()
    logout(request)
    #    except KeyError as e:
    #	return HttpResponseRedirect(reverse('usr:own_profile'))

    request.session['last_logged_user'] = user.id

    return HttpResponseRedirect(reverse('usr:blocked_profile'))


@login_required
def add_previous_education(request):
    p_u = ProfileUpdate(request)

    #try:
    user = p_u.add_new_education()
    #    except KeyError as e:
    #	pass

    return HttpResponseRedirect(reverse('usr:own_profile'))


@user_not_authenticated
@last_logged_user_exists
def blocked_profile(request):
    user = User.objects.get(pk=request.session['last_logged_user'])
    block_code = user.person.block_code

    if block_code == 1:
        return HttpResponseRedirect(reverse('usr:deactivated_profile'))
    elif block_code == 2:
        return HttpResponseRedirect(reverse('usr:new_email_confirmation'))
    elif block_code == 3:
        return HttpResponseRedirect(reverse('usr:register_confirmation'))


@user_not_authenticated
@last_logged_user_exists
def deactivated_profile(request):
    user = User.objects.get(pk=request.session['last_logged_user'])
    return render(request, 'before_login/messages.html',
                  {'user': user, 'type': 'deactivated_profile'})


@user_not_authenticated
@last_logged_user_exists
def new_email_confirmation(request):
    user = User.objects.get(pk=request.session['last_logged_user'])
    return render(request, 'before_login/registration/confirm_email.html', {'user': user})


#confirmation page handling function
@user_not_authenticated
@last_logged_user_exists
def register_confirmation(request):
    user = User.objects.get(pk=request.session['last_logged_user'])
    return render(request, 'before_login/messages.html',
                  {'user': user, 'type': 'registry_confirmation'})


@user_not_authenticated
def register_confirmation_code(request, confirmation_code=None):
    person = get_object_or_404(Person, confirmation_code=confirmation_code)

    user = person.user

    user.person.block_code = 0
    user.person.save()
    user.is_active = True
    user.save()

    return render(
        request,
        'before_login/messages.html',
        {'user': user, 'registration_complete': True,
        'type': 'registry_confirmation_email'})


@login_required
def notifications(request):
    notifications = {
        'unread': request.user.notifications.unread(),
        'read': request.user.notifications.read().order_by('-timestamp')[:10],
    }

    return render(
        request,
        'after_login/usr/notifications.html',
        {'notifications': notifications})

@login_required
@user_is_not_blocked
def notifications_read(request, id=None):
    if id is None:
        raise Http404
    else:
        obj = get_object_or_404(Notification, pk=id, recipient=request.user)
        obj.mark_as_read()

        return HttpResponseRedirect(obj.target.get_absolute_url())


@login_required
@user_is_not_blocked
def app_notifications_save(request):
    if request.POST:
        app_notifications = AppNotifications.objects.get(user=request.user)
        form = AppNotificationsForm(request.POST, instance=app_notifications)
        form.save()

        return HttpResponseRedirect(reverse('usr:own_profile'))
    else:
        raise Http404


@login_required
@user_is_not_blocked
def email_notifications_save(request):
    if request.POST:
        email_notifications = EmailNotifications.objects.get(user=request.user)
        form = EmailNotificationsForm(request.POST, instance=email_notifications)
        form.save()

        return HttpResponseRedirect(reverse('usr:own_profile'))
    else:
        raise Http404