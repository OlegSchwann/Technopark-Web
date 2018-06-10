import question_answer.models as my_db
import question_answer.paginator_lib as paginator  # моя обёртка вокруг django paginator
from django.db import models
import datetime


# -- менеджеры для обработки данных --time
# свежее и горячее
class QuestionManager(models.Manager):
    def __new_questions(self):
        """Return QuerySet of Questions, ordered DEC by time."""
        return my_db.Question.objects \
            .order_by("-time")

    def __best_question(self):
        """Return QuerySet of Questions, ordered DEC by rating, count of Likes."""
        return my_db.Question.objects.order_by("-rating")

    def __taged_question(self, tag):
        """Return QuerySet of Questions on one tag, ordered DEC by rating, count of Likes"""
        return my_db.Question.objects.filter(tags__text=tag).order_by('-rating')

    def __one_question(self, question_id):
        """Return one quersion with id"""
        return my_db.Question.objects.filter(id=question_id).get()

    # Функция, собирающая данные для запроса.
    #     "questions": [
    #         {
    #             "id": "",
    #             "title": "",
    #             "text": "",
    #             "nickname": "",
    #             "avatar_url": "",
    #             "time": "",
    #             "tags": [""],
    #             "rating": 0,
    #             "answers": 0
    #         }
    #     ],
    #     'previous_pages': [1],
    #     'next_pages': [5]
    # принимает QuerySet c нужной выборкой и требуемую страницу.
    def __prepare_data(self, question_array, page_number):
        page = paginator.paginator_wrap(question_array, page_number)
        previous_pages = paginator.five_before(page)
        current_page = page.number
        next_pages = paginator.five_after(page)
        # Проблема: Потратил кучу времени, не смор сделать по нормальному.
        # Надо вытащить связанные данные -
        result = []
        for one_question in page.object_list:
            number_of_answers = my_db.Answer.objects.filter(question_id=one_question.id).count()
            result.append({
                "id": one_question.id,
                "title": one_question.title,
                "text": one_question.text,
                "nickname": one_question.profile_id.user.username,
                "avatar_url": one_question.profile_id.avatar.url,
                "time": one_question.time.strftime("%d %b %y, %H:%M"),  # format: 01 Apr 18, 21:41
                "tags": [i.text for i in one_question.tags.all()],
                "rating": one_question.rating,
                "answers": number_of_answers
            })
        return {
            "questions": result,
            "previous_pages": previous_pages,
            "current_page": current_page,
            "next_pages": next_pages
        }

    # возвращает уже готовый для шаблонизации массив
    def new_questions(self, page_number):
        questions_queryset = self.__new_questions()
        context = self.__prepare_data(questions_queryset, page_number)
        return context

    # возвращает уже готовый для шаблонизации массив
    def best_question(self, page_number):
        questions_queryset = self.__best_question()
        context = self.__prepare_data(questions_queryset, page_number)
        return context

    # возвращает уже готовый для шаблонизации массив
    def tagged_question(self, tag, page_number):
        questions_queryset = self.__taged_question(tag)
        context = self.__prepare_data(questions_queryset, page_number)
        context.update({"tag": tag})
        return context

    # возвращает данные для шаблонизации
    # context = {
    #     "question":
    #         {
    #             "id": "",
    #             "title": "",
    #             "text": "",
    #             "nickname": "",
    #             "avatar_url": "",
    #             "time": "",
    #             "tags": [""],
    #             "rating": 0,
    #         },
    #     "answers": [
    #         {
    #             "id": "",
    #             "text": "",
    #             "nickname": "",
    #             "avatar_url": "",
    #             "time": "",
    #             "rating": 0,
    #             "best_answer": True,
    #         }
    #     ]
    # }
    def prepare_data_for_one_question(self, question_id):
        one_question = self.__one_question(question_id)
        ansver_list = [
            {
                "id": ansver.id,
                "text": ansver.text,
                "nickname": ansver.profile_id.user.username,
                "avatar_url": ansver.profile_id.avatar.url,
                "time": ansver.time,
                "best_answer": ansver.best_answer,
                "rating": ansver.rating
            } for ansver in my_db.Answer.objects.filter(question_id=one_question.id).order_by("-rating").all()
        ]
        question_data = {
            "id": one_question.id,
            "title": one_question.title,
            "text": one_question.text,
            "nickname": one_question.profile_id.user.username,
            "avatar_url": one_question.profile_id.avatar.url,
            "time": one_question.time.strftime("%d %b %y, %H:%M"),  # format: 01 Apr 18, 21:41
            "tags": [i.text for i in one_question.tags.all()],
            "rating": one_question.rating
        }
        return {
            "ansvers": ansver_list,
            "question": question_data
        }

