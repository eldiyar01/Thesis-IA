from django import forms
from django.forms import widgets

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['article', 'content']
        widgets = {
            'article': widgets.HiddenInput(),
            'content': widgets.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Оставьте комментарий'
            }),
        }