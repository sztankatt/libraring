from django import forms
from manager.models import Brainstorm


class BrainstormForm(forms.ModelForm):
    class Meta:
        model = Brainstorm
        exclude = ('datetime_posted',)
        widgets = {
            'comment': forms.Textarea()
        }
