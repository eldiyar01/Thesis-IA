from django.urls import path

from .views import home_test, test_detail, questions, results, maintimer, \
    CreateTestView, UpdateTestView, DeleteTestView

app_name = 'cwt'
urlpatterns = [
    path('', home_test, name='home'),
    path('test-variants/<int:pk>/', test_detail, name='test-variants'),
    path('test-variants/questions/<int:pk>/', questions, name='test-questions'),
    path('test-variants/questions/results/', results, name='test-results'),
    path('timer/', maintimer, name='timer'),

    path('test/create/', CreateTestView.as_view(), name='test-create'),
    path('test/update/<int:pk>/', UpdateTestView.as_view(), name="update-post"),
    path('test/delete/<int:pk>/', DeleteTestView.as_view(), name="delete-post"),
]

