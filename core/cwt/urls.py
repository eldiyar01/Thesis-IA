from django.urls import path, include
from rest_framework import routers

from .views import test_home, test_detail, variant_detail, test_results, \
    CreateTest, UpdateTest, DeleteTest, \
    CreateVariant, UpdateVariant, DeleteVariant, create_question, update_question, DeleteQuestion, search_result

from .viewsets import TestViewSet, VariantViewSet, QuestionViewSet, AnswerViewSet

router = routers.SimpleRouter()
router.register('tests', TestViewSet)
router.register('variants', VariantViewSet)
router.register('questions', QuestionViewSet)
router.register('answers', AnswerViewSet)


app_name = 'cwt'
urlpatterns = [
    path('api/', include(router.urls)),

    path('', test_home, name='home'),
    path('test/<int:pk>/variants/', test_detail, name='test-variants'),
    path('test/variant/<int:pk>/questions/', variant_detail, name='test-questions'),
    path('test/variant/questions/results/', test_results, name='test-results'),

    path('search-result/', search_result, name='search-result'),

    path('test/create/', CreateTest.as_view(), name='test-create'),
    path('test/<int:pk>/update', UpdateTest.as_view(), name="test-update"),
    path('test/<int:pk>/delete/', DeleteTest.as_view(), name="test-delete"),
    path('variant/create/', CreateVariant.as_view(), name='variant-create'),
    path('variant/<int:pk>/update', UpdateVariant.as_view(), name="variant-update"),
    path('variant/<int:pk>/delete/', DeleteVariant.as_view(), name="variant-delete"),
    path('test/<int:test_pk>/variant/<int:variant_pk>/question/create/', create_question, name='question-create'),
    path('test/<int:test_pk>/variant/<int:variant_pk>/question/<int:question_pk>/update',
         update_question, name='question-update'),
    path('test/<int:test_pk>/variant/<int:variant_pk>/question/<int:pk>/delete',
         DeleteQuestion.as_view(), name='question-delete')
]

