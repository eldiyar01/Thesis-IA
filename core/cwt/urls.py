from django.urls import path

from .views import home_test, test_details, questions, results, \
    CreateTestView, UpdateTestView, DeleteTestView, \
    CreateVariantView, UpdateVariantView, DeleteVariantView


app_name = 'cwt'
urlpatterns = [
    path('', home_test, name='home'),
    path('test-variants/<int:pk>/', test_details, name='test-variants'),
    path('test-variants/questions/<int:pk>/', questions, name='test-questions'),
    path('test-variants/questions/results/', results, name='test-results'),

    path('test/create/', CreateTestView.as_view(), name='test-create'),
    path('test/update/<int:pk>/', UpdateTestView.as_view(), name="test-update"),
    path('test/delete/<int:pk>/', DeleteTestView.as_view(), name="test-delete"),
    path('variant/create/', CreateVariantView.as_view(), name='variant-create'),
    path('variant/update/<int:pk>/', UpdateVariantView.as_view(), name="variant-update"),
    path('variant/delete/<int:pk>/', DeleteVariantView.as_view(), name="variant-delete"),
]

