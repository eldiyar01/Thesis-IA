from django.urls import path, include
from rest_framework import routers

from .views import home_test, test_details, questions, results, \
    CreateTestView, UpdateTestView, DeleteTestView, \
    CreateVariantView, UpdateVariantView, DeleteVariantView, create_question, update_question, search_result

from .viewsets import TestViewSet, VariantViewSet, QuestionViewSet, AnswerViewSet

router = routers.SimpleRouter()
router.register('test', TestViewSet)
router.register('variant', VariantViewSet)
router.register('question', QuestionViewSet)
router.register('answer', AnswerViewSet)


app_name = 'cwt'
urlpatterns = [
    path('api/', include(router.urls)),

    path('', home_test, name='home'),
    path('test-variants/<int:pk>/', test_details, name='test-variants'),
    path('test-variants/questions/<int:pk>/', questions, name='test-questions'),
    path('test-variants/questions/results/', results, name='test-results'),

    path('search-result/', search_result, name='search-result'),

    path('test/create/', CreateTestView.as_view(), name='test-create'),
    path('test/update/<int:pk>/', UpdateTestView.as_view(), name="test-update"),
    path('test/delete/<int:pk>/', DeleteTestView.as_view(), name="test-delete"),
    path('variant/create/', CreateVariantView.as_view(), name='variant-create'),
    path('variant/update/<int:pk>/', UpdateVariantView.as_view(), name="variant-update"),
    path('variant/delete/<int:pk>/', DeleteVariantView.as_view(), name="variant-delete"),
    path('variant/question_create/<int:pk>/', create_question, name='create-question'),
    path('variant/question_update/<int:variant_pk>/<int:question_pk>', update_question, name='update-question')
]

