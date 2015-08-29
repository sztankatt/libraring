from django import forms
from django.utils.translation import ugettext_lazy as _


class BrainstormForm(forms.Form):
    name = forms.CharField(
        required=True, label=_('Your name'))
    email = forms.EmailField(
        required=True, label=_('Your e-mail'))
    comment = forms.CharField(
        required=True, label=_('Comment'),
        widget=forms.Textarea)
