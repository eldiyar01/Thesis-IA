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


def test_detail(request, pk):
    test_variants = Test.objects.get(id=pk)
    return render(request, 'cwt/test_variants.html', {'test': test_variants})


@login_required
def questions(request, pk):
    v_questions = Variant.objects.get(id=pk)
    return render(request, 'cwt/test_questions.html', {'v_questions': v_questions})


def maintimer(request):
    pass


def results(request):
    user = request.user
    post = request.POST.items()
    for question, answer in post:
        if 'question-' in question:
            _, question_pk = question.split('-')
            answers = Answer.objects.filter(question=question_pk)
            correct_answer = answers.get(is_correct=True)
            user_choose = Answer.objects.filter(id=answer)[0]
            answer_point = Question.objects.get(id=question_pk).points
            # Question.objects.filter(id=question_pk).points
            print('ответы', answers)
            print('правильные ответы', correct_answer)
            print('выбор польз', user_choose)
            print('баллы', answer_point)
            if correct_answer == user_choose:
                print('write')

            else:
                print('wrong')
    return render(request, 'cwt/test_results.html', )


class CreateTestView(CreateView):
    model = Test
    template_name = 'cwt/cr_udt_test.html'
    form_class = TestForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdateTestView(UpdateView):
    model = Test
    template_name = 'crud/cr_udt_test.html'
    form_class = TestForm


class DeleteTestView(DeleteView):
    model = Test
    template_name = 'crud/delete_test.html'


