from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View


from .models import Question, Variant, Test, Answer


def home_test(request):
    tests = Test.objects.all()
    return render(request, 'cwt/test_home.html', {'tests': tests})


def test_detail(request, pk):
    test_variants = Test.objects.get(id=pk)
    return render(request, 'cwt/test_variants.html', {'test': test_variants})


def questions(request, pk):
    v_questions = Variant.objects.get(id=pk)
    total_questions = v_questions.questions.count()
    user = request.user
    return render(request, 'cwt/test_questions.html', {'v_questions': v_questions})


def results(request):
    question = request.GET
    user = request.user


    print(request.GET)
    print(user)
    print(question)
    return render(request, 'cwt/test_results.html', {'q': question})
    # else:
    #     return redirect('cwt:test-questions')





#question = request.GET.get('question-{{ question.pk }}')
# if question == '{{ ans.pk }}':
#     print('write')
#     return render(request, 'cwt/test_home.html')
