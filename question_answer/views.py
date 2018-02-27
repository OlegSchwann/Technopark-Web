from django.shortcuts import render

# Create your views here.

# главная страница '/'
# показывает заданные вопросы списком


def hot_questions(request):
    return render(request, 'question_answer/hot_questions.html', {})

