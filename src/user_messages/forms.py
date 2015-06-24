from django.forms import ModelForm
from django import forms

from .models import Message

class MessageForm(ModelForm):
    
    class Meta:
        model = Message
        exclude = ('send_date', 'seen')
        widgets = {
            'transaction' : forms.HiddenInput(),
            'sender' : forms.HiddenInput(),
            'text': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Type text here...'})
        }