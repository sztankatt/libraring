from django.forms import ModelForm
from usr.models import Person, Class, Institution, Location, COUNTRIES, alphanumeric_regex
from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _
from datetimewidget.widgets import DateWidget



class RegisterPersonForm(ModelForm):

    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder':'e-mail'}))
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    #date_born = forms.DateField(required=False, input_formats=DATE_INPUT_FORMATS, label='DD/MM/YYYY')

    #location model parts
    country 			= forms.ChoiceField(choices=[('','---------')]+COUNTRIES)
    postcode			= forms.CharField(max_length=10, required=False, validators=[alphanumeric_regex])
    city				= forms.CharField(max_length=50)

    class Meta:
        datetimeOptions ={
            'format':'dd/mm/yyyy',
            'autoclose':True,
            'showMeridian':True,
            'startView':4,
        }
        model = Person
        exclude = ('user', 'person_type', 'current_education', 'education', 'institution', 'confirmation_code',
                   'block_code','location')
        widgets = {  # 'person_type' : forms.RadioSelect(),
                     'about': forms.Textarea(),
                     'date_born': DateWidget(attrs={'id':"yourdatetimeid"}, usel10n = True, bootstrap_version=3, options=datetimeOptions)
        }

class ClassForm(ModelForm):
    #email = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'e-mail' \
    #    , 'class': 'form-control profile-update-input'}))
    terms_conditions = forms.BooleanField()

    class Meta:
        model = Class
        fields = '__all__'


class NClassForm(ClassForm):
    pass


class InstitutionForm(forms.Form):
    institution = forms.ModelChoiceField(Institution.objects,
                                         required=True,
                                         widget=forms.Select(attrs={}))
    email = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'e-mail'}))


class UserCreationForm(auth_forms.UserCreationForm):
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    username = forms.RegexField(label=_("Username"), max_length=30,
                                regex=r'^[\w.-]+$',
                                help_text=_("Required. 30 characters or fewer. Letters, digits and "
                                            "./-/_ only."),
                                error_messages={
                                    'invalid': _("This value may contain only letters, numbers and "
                                                 "./-/_ characters.")})

    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput())
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput(),
                                help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ("username",)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, \
                               widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(max_length=50, \
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
		