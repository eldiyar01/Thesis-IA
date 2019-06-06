from rest_framework import permissions, viewsets

from .models import Test, Variant, Question, Answer
from .serializers import TestSerializer, VariantSerializer, QuestionSerializer, AnswerSerializer
from .filters import TestFilter


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    filter_class = TestFilter
    permission_classes = [permissions.AllowAny]


class VariantViewSet(viewsets.ModelViewSet):
    queryset = Variant.objects.all()
    serializer_class = VariantSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

