from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets

from .models import Test, Variant, Question


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'time', 'description', 'image']
        widgets = {
            'title': widgets.TextInput(attrs={'class': 'form-control'}),
            'description': widgets.Textarea(attrs={'class': 'form-control'}),
            'time': widgets.NumberInput(attrs={'class': 'form-control'})
        }


class VariantForm(forms.ModelForm):
    class Meta:
        model = Variant
        fields = ['test', 'title', 'description']
        widgets = {
            'test': widgets.Select(attrs={'class': 'custom-select'}),
            'title': widgets.TextInput(attrs={'class': 'form-control'}),
            'description': widgets.Textarea(attrs={'class': 'form-control'})
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'points']
        widgets = {
            'text': widgets.TextInput(attrs={'class': 'form-control'}),
            'points': widgets.NumberInput(attrs={'class': 'form-control'})
        }


class AnswersForm(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()
        has_one_correct_answer = False
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct', False):
                    has_one_correct_answer = True
                    break
        if not has_one_correct_answer:
            raise ValidationError('Ошибка. Вы не указали правильный ответ', code='no_correct_answer')



