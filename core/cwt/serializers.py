from rest_framework import serializers

from .models import Test, Variant, Question, Answer


class TestSerializer(serializers.ModelSerializer):
    variants = serializers.StringRelatedField(many=True)

    class Meta:
        model = Test
        fields = ['pk', 'title', 'description', 'image', 'variants']


class VariantSerializer(serializers.ModelSerializer):
    questions = serializers.StringRelatedField(many=True)

    class Meta:
        model = Variant
        fields = ['pk', 'title', 'description', 'tests', 'questions']

    # def get_count(self, obj):
    #    return obj.questions.count()


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['pk', 'title', 'points', 'variants']


class AnswerSerializer(serializers.ModelSerializer):
    # question = serializers.StringRelatedField(read_only=False)

    class Meta:
        model = Answer
        fields = ['pk', 'text', 'is_correct', 'question']

