from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView

from .forms import TestForm, QuestionForm, AnswersForm
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


# logic of getting variant.all_question.correct_answers and == user.answers
def results(request):
    user = request.user
    test = None
    user_points = []
    all_points = []
    all_questions = []
    question_answer = {}
    for question, answer in request.POST.items():
        if 'question-' in question:
            _, question_pk = question.split('-')
            question = Question.objects.get(pk__in=question_pk)
            # .prefetch_related('answers')
            all_questions.append(question)
            question_answer[int(question_pk)] = int(answer)
            test = Test.objects.get(id=question.variants.tests.id)
    for q in all_questions:
        all_points.append(q.points)
        if q.correct_answer.id == question_answer[q.id]:
            user_points.append(q.points)
    sum_user_points = sum(user_points)
    all_points_sum = sum(all_points)
    UserResult.objects.create(user=user, scores=sum_user_points, test=test, variant_scores=all_points_sum)

    if sum_user_points > sum_user_points//2 and sum_user_points < all_points_sum:
        message = 'Вы молодец! Вы можете получить золотой сертификат'
    elif sum_user_points == all_points_sum or sum_user_points > (sum_user_points-10):
        message = 'Отлично! Можете считать, что золотой сертификат у вас в руках ;)'
    else:
        message = 'Вам следует уделять больше внимание учебе!'
    print(dir(sum_user_points))
    print(sum_user_points)
    context = {'message': message, 'user': user,
               'user_points': sum_user_points, 'all_points': all_points_sum}
    return render(request, 'cwt/test_results.html', context)


def search_result(request):
    search_q = request.GET.get('search')
    if search_q:
        test_search_r = Test.objects.filter(title__icontains=search_q)
    else:
        test_search_r = "Извините, но по вашему запросу мы ничего не нашли :("
    return render(request, 'cwt/search_result.html', context={'res_tests': test_search_r,
                                                              'search': search_q})


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


def create_question(request, pk):
    variant = get_object_or_404(Variant, id=pk)
    if request.method == 'POST':
        form = QuestionForm
        if form.is_valid():
            question = form.save(commit=False)
            question.variants = variant
            question.save()
            return redirect('cwt:update-question', variant.pk, question.pk)


def update_question(request, pk):
    variant = get_object_or_404(Variant, id=pk)
    question = get_object_or_404(Question, id=pk)

    AnswerFormSet = inlineformset_factory(
        Question,
        Answer,
        formset=AnswersForm,
        fields=('text', 'is_correct'),
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
            return redirect()
        else:
            form = QuestionForm(instance=question)
            formset = AnswerFormSet(instance=question)
        return render(request, 'crud/update_question.html', {'variant': variant,
                                                             'question': question,
                                                             'form': form,
                                                             'formset': formset})

