from django.shortcuts import render
import question_answer.paginator_lib # моя обёртка вокруг django paginator

# Create your views here.

# главная страница '/'
# показывает заданные вопросы списком
def hot_questions(request, page=1):
    # сначала просто заглушки - литеральные константы
    context = {
        "popular_tags": [
            "perl",
            "python",
            "tehnopark",
            "mysql",
            "django",
            "mail.ru",
            "firefox"
        ],
        "best_members": [
            "Mr.Freeman",
            "Dr.Horse",
            "Bender",
            "V.Pupkin"
        ],
        "questions": [
            {
                "id": x,
                "title": "{}-й вопрос.".format(x),
                "text": "Привет! Я тут делаю сайтик на Django, для курса по web. Собственно, вокруг. "
                        "Как бы улучшить, чтоб нормально работало и было адекватным в использовании?",
                "nickname": "Max",
                "time": "25 марта",
                "tags": ["Django", "Python", "Разработка интерфейсов", "css"],
                "rating": 0,
                "ansvers": 0
            } for x in range(1, 101)
        ]
    }
    context["questions"] = page = question_answer.paginator_lib.paginator_wrap(
        context["questions"], page
    )
    context['previous_pages'] = question_answer.paginator_lib.five_before(page)
    context['next_pages'] = question_answer.paginator_lib.five_after(page)
    return render(request, 'question_answer/hot_questions.html', context=context)


def all_questions(request):
    return render(request, 'question_answer/all_questions.html', {})


def adding_question(request):
    return render(request, 'question_answer/adding_question.html', {})


# форма регистрации
def register_page(request):
    return render(request, 'question_answer/registration_form.html', {})


# форма входа
def authorization_page(request):
    return render(request, 'question_answer/authorization_form.html', {})


# страница одного вопроса
def one_question_page(request, question_id=1):
    return render(request, 'question_answer/one_question_page.html', {})


# страница вопросов по одному тегу
def one_tag_page(request, tag=''):
    return render(request, 'question_answer/one_tag_page.html', {})


# страница настроек пользователя
def user_settings(request):
    return render(request, 'question_answer/user_settings.html', {})
