from django.urls import path, re_path, include
from rest_framework import routers

from .views import home, LoginView, SignUpConfirmView, SignupDoneView, SignupView, LogoutView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView, \
    PasswordChangeView, PasswordChangeDoneView, \
    FeedbackView

from .viewsets import UserViewSet


router = routers.SimpleRouter()
router.register('users', UserViewSet)


app_name = 'user'
urlpatterns = [
    path('api/', include(router.urls)),

    path('', home, name='profile-home'),
    path('signin/', LoginView.as_view(), name='signin'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('signup/done/', SignupDoneView.as_view(), name='signup-done'),
    re_path(
        r'^signup/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        SignUpConfirmView.as_view(),
        name='signup-confirm',
    ),

    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('password-reset/done', PasswordResetDoneView.as_view(), name='password-reset-done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('password-reset/complete', PasswordResetCompleteView.as_view(), name='password-reset-complete'),
    path('password-change/', PasswordChangeView.as_view(), name='password-change'),
    path('password-change/done', PasswordChangeDoneView.as_view(), name='password-change-done'),

    path('feedback/', FeedbackView.as_view(), name='feedback')
]
