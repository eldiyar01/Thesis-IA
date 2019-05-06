from django.urls import path

from .views import home_test, test_detail, questions, results

app_name = 'cwt'
urlpatterns = [
    path('', home_test, name='home'),
    path('test-variants/<int:pk>/', test_detail, name='test-variants'),
    path('test-variants/questions/<int:pk>/', questions, name='test-questions'),
    path('test-variants/questions/results/', results, name='test-results')
]

