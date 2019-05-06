from django.urls import path, re_path

from .views import LoginView, SignUpConfirmView, SignupDoneView, SignupView, home, logout, \
    PasswordReset, PasswordResetDone, PasswordResetComplete, PasswordResetConfirm

app_name = 'user'
urlpatterns = [
    path('', home, name='profile_home'),
    path('signin/', LoginView.as_view(), name='signin'),
    path('logout/', logout, name='logout'),

    path('signup/', SignupView.as_view(), name='signup'),
    path('signup/done/', SignupDoneView.as_view(), name='signup-done'),
    re_path(
        r'^signup/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        SignUpConfirmView.as_view(),
        name='signup-confirm',
    ),

    path('password-reset/', PasswordReset.as_view(), name='password-reset'),
    path('password-reset/done', PasswordResetDone.as_view(), name='password-reset-done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password-reset-confirm'),
    path('password-reset/complete', PasswordResetComplete.as_view(), name='password-reset-complete')
]
