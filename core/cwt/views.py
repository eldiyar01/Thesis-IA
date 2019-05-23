from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView

from .forms import TestForm
from .models import Question, Variant, Test, Answer, UserResult


def home_test(request):
    tests = Test.objects.all()
    return render(request, 'cwt/test_home.html', {'tests': tests})


def test_details(request, pk):
    test_variants = Test.objects.get(id=pk)
    return render(request, 'cwt/test_variants.html', {'test': test_variants})


def questions(request, pk):
    v_questions = Variant.objects.get(id=pk)
    return render(request, 'cwt/test_questions.html', {'v_questions': v_questions})


def results(request):
    user = request.user
    user_points = []
    all_points = []
    all_questions = []
    question_answer = {}
    #logic of getting variant.all_question.correct_answers and == user.answers
    for question, answer in request.POST.items():
        if 'question-' in question:
            _, question_pk = question.split('-')
            question = Question.objects.get(pk__in=question_pk)
            # .prefetch_related('answers')
            all_questions.append(question)
            question_answer[int(question_pk)] = int(answer)
    for q in all_questions:
        all_points.append(q.points)
        if q.correct_answer.id == question_answer[q.id]:
            user_points.append(q.points)
    sum_user_points = sum(user_points)
    all_points_sum = sum(all_points)
    UserResult.objects.create(user=user, scores=sum_user_points)
    if sum_user_points > 110 and sum_user_points < 200:
        message = 'Вы молодец! Вы можете получить золотой сертификат'
    elif sum_user_points > 200:
        message = 'Отлично! Можете считать, что золотой сертификат у вас в руках ;)'
    else:
        message = 'Вам следует уделять больше внимание учебе!'
    context = {'message': message, 'user': user,
               'user_points': sum_user_points, 'all_points': all_points_sum}
    return render(request, 'cwt/test_results.html', context)


class CreateTestView(CreateView):
    model = Test
    template_name = 'crud/cr_upd_test.html'
    form_class = TestForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdateTestView(UpdateView):
    model = Test
    template_name = 'crud/cr_upd_test.html'
    form_class = TestForm


class DeleteTestView(DeleteView):
    model = Test
    template_name = 'crud/delete_test.html'


class CreateVariantView(CreateView):
    model = Variant
    template_name = 'crud/cr_upd_variant.html'


class UpdateVariantView(UpdateView):
    model = Variant
    template_name = 'crud/cr_upd_variant.html'


class DeleteVariantView(DeleteView):
    model = Variant
    template_name = 'crud/delete_variant.html'


class CreateQuestionView(CreateView):
    model = Question
    template_name = 'crud/cr_upd_question.html'


class UpdateQuestionView(UpdateView):
    model = Question
    template_name = 'crud/cr_upd_question.html'


class DeleteQuestionsView(DeleteView):
    model = Question
    template_name = 'crud/delete_question'


class CreateAnswerView(CreateView):
    pass


class UpdateAnswerView(UpdateView):
    pass


class DeleteAnswerView(DeleteView):
    pass

