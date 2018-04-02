from django.shortcuts import render
import question_answer.paginator_lib  # моя обёртка вокруг django paginator
import question_answer.data_prepearing as data_prepearing

prepearer = data_prepearing.QuestionManager()


# Create your views here.


# главная страница '/'
# показывает заданные вопросы списком
def hot_questions(request, page=1):
    context = prepearer.new_questions(page_number=page)
    return render(request, 'question_answer/hot_questions.html', context=context)


def all_questions(request, page=1):
    context = prepearer.best_question(page_number=page)
    return render(request, 'question_answer/all_questions.html', context=context)


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
    # заглушка
    # context = {
    #     "popular_tags": ["half", "again", "travel", "book"],
    #     "best_members": ["wgarcia", "lindseyclifford", "linda89"],
    #     "question":
    #         {
    #             "id": "1",
    #             "title": "1st_question",
    #             "text": "Lorem ipsum",
    #             "nickname": "loem",
    #             "time": "12:00",
    #             "tags": ["half", "again", "travel", "book"],
    #             "rating": 0,
    #         },
    #     "ansvers": [
    #         {
    #             "id": "1",
    #             "text": "lorem",
    #             "nickname": "loremer",
    #             "time": "13:01",
    #             "rating": 0,
    #             "best_answer": True,
    #         },
    #         {
    #             "id": "1",
    #             "text": "lorem",
    #             "nickname": "loremer",
    #             "time": "13:01",
    #             "rating": 0,
    #             "best_answer": False,
    #         }
    #     ]
    # }

    context = prepearer.prepare_data_for_one_question(question_id)
    return render(request, 'question_answer/one_question_page.html', context=context)


# страница вопросов по одному тегу
def one_tag_page(request, tag, page=1):
    context = prepearer.tagged_question(tag=tag, page_number=page)
    return render(request, 'question_answer/one_tag_page.html', context=context)


# страница настроек пользователя
def user_settings(request):
    return render(request, 'question_answer/user_settings.html', {})
