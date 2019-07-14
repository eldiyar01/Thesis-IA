from django import forms
from django.forms import widgets

from .models import Comment, Article, Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title']
        widgets = {
            'title': widgets.TextInput(attrs={'class': 'form-control'}),
            }


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['category', 'title', 'description', 'content', 'image']
        widgets = {
            'category': widgets.Select(attrs={'class': 'custom-select'}),
            'title': widgets.TextInput(attrs={'class': 'form-control'}),
            'description': widgets.Textarea(attrs={'class': 'form-control'}),
            'content': widgets.Textarea(attrs={'class': 'form-control'}),
        }


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