from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.forms import inlineformset_factory, widgets
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from .forms import TestForm, QuestionForm, AnswersForm, VariantForm
from .models import Question, Variant, Test, Answer, UserResult


def test_home(request):
    tests = Test.objects.all()
    return render(request, 'cwt/test_home.html', {'tests': tests})


def test_detail(request, pk):
    test = Test.objects.get(id=pk)
    return render(request, 'cwt/test_variants.html', {'test': test})


@login_required
def variant_detail(request, pk):
    variant = Variant.objects.get(id=pk)
    return render(request, 'cwt/test_questions.html', {'variant': variant})


@login_required
def test_results(request):
    user = request.user
    test = None
    user_points = []
    all_points = []
    all_questions = []
    question_answer = {}
    for question, answer in request.POST.items():
        if 'question-' in question:
            _, question_pk = question.split('-')
            question = Question.objects.get(id=question_pk)
            all_questions.append(question)
            question_answer[int(question_pk)] = int(answer)
            test = Test.objects.get(id=question.variant.test.id)

    for question in all_questions:
        all_points.append(question.points)
        if question.correct_answer.id == question_answer[question.id]:
            user_points.append(question.points)

    sum_user_points = sum(user_points)
    all_points_sum = sum(all_points)
    UserResult.objects.create(user=user, scores=sum_user_points, test=test, variant_scores=all_points_sum)

    if sum_user_points >= (all_points_sum//1.1):
        message = 'Отлично! Вы молодец ;)'
    elif sum_user_points > (sum_user_points // 2):
        message = 'Неплохо! Но можно и лучше'
    else:
        message = 'Вам следует уделять больше внимание учебе!'
    context = {'message': message, 'user': user,
               'user_points': sum_user_points, 'all_points': all_points_sum}

    return render(request, 'cwt/test_results.html', context)


def search_result(request):
    search_q = request.GET.get('search')
    if search_q == '':
        return redirect('home')
    elif search_q:
        test_search_r = Test.objects.filter(title__icontains=search_q)
    else:
        test_search_r = "Извините, но по вашему запросу мы ничего не нашли :("
    return render(request, 'cwt/search_result.html', context={'res_tests': test_search_r,
                                                              'search': search_q})


class CreateTest(PermissionRequiredMixin, CreateView):
    permission_required = ("is_staff", "is_superuser",)
    model = Test
    template_name = 'cwt/crud/cr_upd_test.html'
    form_class = TestForm


class UpdateTest(PermissionRequiredMixin, UpdateView):
    permission_required = ("is_staff", "is_superuser",)
    model = Test
    template_name = 'cwt/crud/cr_upd_test.html'
    form_class = TestForm

    def get_success_url(self):
        return reverse('cwt:home')


class DeleteTest(PermissionRequiredMixin, DeleteView):
    permission_required = ("is_staff", "is_superuser",)
    model = Test
    template_name = 'cwt/crud/delete_test.html'
    success_url = reverse_lazy('cwt:home')


class CreateVariant(PermissionRequiredMixin, CreateView):
    permission_required = ("is_staff", "is_superuser",)
    model = Variant
    form_class = VariantForm
    template_name = 'cwt/crud/cr_upd_variant.html'


class UpdateVariant(PermissionRequiredMixin, UpdateView):
    permission_required = ("is_staff", "is_superuser",)
    model = Variant
    form_class = VariantForm
    template_name = 'cwt/crud/cr_upd_variant.html'

    def get_success_url(self):
        variant = self.get_object()
        return reverse('cwt:test-variants', kwargs={'pk': variant.test_id})


class DeleteVariant(PermissionRequiredMixin, DeleteView):
    permission_required = ("is_staff", "is_superuser",)
    model = Variant
    template_name = 'cwt/crud/delete_variant.html'

    def get_success_url(self):
        variant = self.get_object()
        return reverse('cwt:test-variants', kwargs={'pk': variant.test_id})


@login_required
def create_question(request, test_pk, variant_pk):
    test = get_object_or_404(Test, id=test_pk)
    variant = get_object_or_404(Variant, id=variant_pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.variant = variant
            question.variant.test = test
            question.save()
            return redirect('cwt:question-update', test_pk, variant.pk, question.pk)
    else:
        form = QuestionForm
    return render(request, 'cwt/crud/create_question.html', {'variant': variant, 'form': form})


@login_required
def update_question(request, test_pk, variant_pk, question_pk):
    test = get_object_or_404(Test, id=test_pk)
    variant = test = get_object_or_404(Test, id=test_pk)
    variant = get_object_or_404(Variant, id=variant_pk, test=test)
    question = get_object_or_404(Question, id=question_pk, variant__test=test, variant=variant)

    AnswerFormSet = inlineformset_factory(
        Question,
        Answer,
        formset=AnswersForm,
        fields=('text', 'is_correct'),
        widgets={'text': widgets.TextInput(attrs={'class': 'form-control'})},
        min_num=2,
        validate_min=True,
        max_num=5,
        validate_max=True,
    )

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = AnswerFormSet(request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()
            return redirect('cwt:test-questions', variant.pk)
    else:
        form = QuestionForm(instance=question)
        formset = AnswerFormSet(instance=question)
    return render(request, 'cwt/crud/update_question.html', {'test': test,
                                                         'variant': variant,
                                                         'question': question,
                                                         'form': form,
                                                         'formset': formset})


class DeleteQuestion(PermissionRequiredMixin, DeleteView):
    permission_required = ("is_staff", "is_superuser",)
    model = Question
    template_name = 'cwt/crud/delete_question.html'

    def get_success_url(self):
        question = self.get_object()
        return reverse('cwt:test-questions', kwargs={'pk': question.variant_id})
