from django import forms
from django.forms import widgets

from .models import Test


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'description', 'image']
        widgets = {
            'title': widgets.TextInput(attrs={'class': 'form-control'}),
            'description': widgets.Textarea(attrs={'class': 'form-control'})
        }



class AnswersForm(forms.ModelForm):
    pass


