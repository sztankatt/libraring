from django.forms import ModelForm
from usr.models import Person, Class, Institution
from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _

class RegisterPersonForm(ModelForm):
	DATE_INPUT_FORMATS = [
		'%d/%m/%Y'	
	]
	
	#email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder':'e-mail'}))
	first_name = forms.CharField(max_length=100, required=True)
	last_name = forms.CharField(max_length=100, required=True)
	date_born = forms.DateField(required=False, input_formats=DATE_INPUT_FORMATS, label='DD/MM/YYYY')
	
	class Meta:
		model = Person
		exclude = ('user','person_type','current_education', 'education', 'institution', 'date_born', 'confirmation_code', 'block_code')
		widgets = {
			#'person_type' : forms.RadioSelect(),
			'about': forms.Textarea(),
		}
		

class ClassForm(ModelForm):
	email 		=forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder':'e-mail'\
				, 'class': 'form-control profile-update-input'}))
	terms_conditions = forms.BooleanField()
	class Meta:
		model = Class


class NClassForm(ClassForm):
	def __init__(self, *args, **kwargs):
		super(ClassForm, self).__init__(*args, **kwargs)
		self.fields.pop('email')

class InstitutionForm(forms.Form):
	institution 	= forms.ModelChoiceField(Institution.objects,
				required=True,
				widget=forms.Select(attrs={}))
	email 		=forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder':'e-mail'}))
	
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
				   widget=forms.TextInput(attrs={'placeholder':'Username'}))
	password = forms.CharField(max_length=50, \
				   widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
		