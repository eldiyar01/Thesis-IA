from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UsernameField, AuthenticationForm, SetPasswordForm, PasswordChangeForm
from django.core.mail import send_mail
from django.forms import widgets
from django.template.loader import render_to_string
from django.utils.translation import gettext, gettext_lazy as _


class UserCreationForm(forms.ModelForm):
    username = UsernameField(
        label=('Имя пользователя'),
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control',
                                      'placeholder': 'Имя под которым вы будете заходить на сайт'}),
    )
    email = forms.EmailField(
        label=('Электронная почта'),
        required=True,
        widget=widgets.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Например: eko@gmail.com'
        }),
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password',)
        widgets = {
            'password': widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Придумайте пароль'}),
        }

    def clean_email(self):
        email = self.cleaned_data["email"]
        users_found = get_user_model().objects.filter(email__iexact=email).exists()

        if users_found:
            raise forms.ValidationError("Пользователь с таким именем уже существует")
        return email

    def save(self):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.email = self.cleaned_data["email"]
        user.is_active = False
        user.save()
        return user


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )


class PasswordChangeFormCustom(PasswordChangeForm, SetPasswordForm):
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': True, 'class': 'form-control'}),
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )


class FeedbackForm(forms.Form):
    name = forms.CharField(label=("Имя"),
                           widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control',
                                                         'placeholder': 'Имя пользователя'}))
    subject = forms.CharField(label=("Тема"),
                              widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control',
                                                            'placeholder': 'По какому поводу пишется письмо'}))
    email = forms.EmailField(label=("Электронная почта"),
                             widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control',
                                                           'placeholder': 'Ваш адрес электронной почты'}))
    message = forms.CharField(label=("Письмо"),
                              widget=forms.Textarea(attrs={'rows': 8, 'cols': 40,
                                                           'autofocus': True, 'class': 'form-control',
                                                           'placeholder': 'Собственно говоря само письмо'}))

    def send_email(self):
        c_d = self.cleaned_data
        send_mail(
            subject=c_d.get('subject'),
            message=render_to_string(
                'feedback_email/email.html',
                {
                    'name': c_d.get('name'),
                    'message': c_d.get('message'),
                    'email': c_d.get('email')
                }
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['energeticbinge@gmailcom'],
            fail_silently=True
        )
