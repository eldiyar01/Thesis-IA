from django.conf import settings
from django.contrib.auth import get_user_model, login, views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.http import base36_to_int, int_to_base36
from django.utils.translation import ugettext_lazy as _
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView

from .forms import UserCreationForm, LoginForm, FeedbackForm, PasswordChangeFormCustom


@login_required
def home(request):
    return render(request, 'profile/home.html')


class LogoutView(auth_views.LogoutView):
    template_name = 'user/logout.html'


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'user/login.html'


class SignupView(CreateView):
    template_name = 'user/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('user:signup-done')

    def form_valid(self, form):
        ret = super().form_valid(form)
        site_name = 'Local Forum'
        domain = 'localhost'
        uid = int_to_base36(self.object.id)
        token = default_token_generator.make_token(self.object)
        mail_context = {
            'email': self.object.email,
            'domain': domain,
            'site_name': site_name,
            'uid': uid,
            'user': self.object,
            'token': token,
            'url': self.request.build_absolute_uri(reverse(
                'user:signup-confirm',
                kwargs={'uidb36': uid, 'token': token}
            ))
        }

        send_mail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.object.email],
            message='',
            subject=_('Спасибо, ваша регистрация прошла успешно!'),
            html_message=render_to_string(template_name='user/email/signup.html', context=mail_context),
        )
        return ret


class SignupDoneView(TemplateView):
    template_name = 'user/signup_done.html'


class SignUpConfirmView(View):
    def get(self, request, *args, **kwargs):
        uidb36 = kwargs.get('uidb36')
        token = kwargs.get('token')
        try:
            uid_int = base36_to_int(uidb36)
        except ValueError:
            raise Http404

        user = get_object_or_404(get_user_model(), id=uid_int)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()

        login(request, user=user)
        return redirect('cwt:home')


class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'user/password/reset.html'
    email_template_name = 'user/password/reset_email.html'
    success_url = reverse_lazy('user:password-reset-done')


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'user/password/done.html'


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'user/password/reset_confirm.html'
    success_url = reverse_lazy('user:password-reset-complete')


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'user/password/reset_complete.html'


class PasswordChangeView(auth_views.PasswordChangeView):
    form_class = PasswordChangeFormCustom
    success_url = reverse_lazy('user:password-change-done')
    template_name = 'user/password/password_change_form.html'


class PasswordChangeDoneView(auth_views.PasswordResetDoneView):
    template_name = 'user/password/password_change_done.html'


class FeedbackView(FormView):
    template_name = 'feedback_email/email_form.html'
    form_class = FeedbackForm
    success_url = reverse_lazy('user:profile-home')

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)

