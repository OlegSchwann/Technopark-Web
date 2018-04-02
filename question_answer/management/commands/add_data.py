from django.core.management.base import BaseCommand
import question_answer.models as my_db
import faker
import random

fake = faker.Faker()


def create_user():
    one_user = my_db.User.objects.create_user(
        username=fake.user_name(),
        email=fake.email(),
        password=fake.word()
    )
    one_user.profile.avatar_link = 'http://localhost:8080/static/avatar.jpeg'
    one_user.save()
    print("one_user.id = ", one_user.id)


def create_question():
    # получаем случайный валидный профиль
    all_profile = my_db.Profile.objects.all()
    random_profile = all_profile[random.randint(0, all_profile.__len__() - 1)]
    new_question = my_db.Question.objects.create(
        title=fake.bs(),
        text=fake.text(max_nb_chars=400),
        profile_id=random_profile,
        time=fake.date_time_between_dates(datetime_start=None, datetime_end=None, tzinfo=None)
    )
    new_question.save()


def create_answer():
    # получаем случайный валидный вопрос
    all_question = my_db.Question.objects.all()
    random_question = all_question[random.randint(0, all_question.__len__() - 1)]

    all_profiles = my_db.Profile.objects.all()
    random_profile = all_profiles[random.randint(0, all_profiles.__len__() - 1)]

    new_answer = my_db.Answer.objects.create(
        text=fake.text(max_nb_chars=random.randint(20, 200)),
        profile_id=random_profile,
        question_id=random_question,
        time=fake.date_time_between_dates(datetime_start=None, datetime_end=None, tzinfo=None),
        best_ansver=True if (random.random() < 0.1) else False
    )
    new_answer.save()
    print("new_answer = ", new_answer.id)


def create_question_like():
    # получаем случайный валидный вопрос
    all_question = my_db.Question.objects.all()
    random_question = all_question[random.randint(0, all_question.__len__() - 1)]
    # получаем случайный валидный профиль
    all_profile = my_db.Profile.objects.all()
    random_profile = all_profile[random.randint(0, all_profile.__len__() - 1)]

    like_status = 1 if random.random() > 0.3 else -1

    new_question_like = my_db.QuestionLike.objects.create(
        profile_id=random_profile,
        question_id=random_question,
        status=like_status  # + or -
    )
    new_question_like.save()

    random_question.rating += like_status
    random_question.save()

    print("question_like ", new_question_like.id)


def create_answer_like():
    # получаем случайный валидный ответ
    all_answer = my_db.Answer.objects.all()
    random_answer = all_answer[random.randint(0, all_answer.__len__() - 1)]
    # получаем случайный валидный профиль
    all_profile = my_db.Profile.objects.all()
    random_profile = all_profile[random.randint(0, all_profile.__len__() - 1)]

    like_status = 1 if random.random() > 0.3 else -1

    new_answer_like = my_db.AnswerLike.objects.create(
        profile_id=random_profile,
        answer_id=random_answer,
        status=like_status
    )
    new_answer_like.save()

    random_answer.rating += like_status
    random_answer.save()
    print("answer_like ", new_answer_like.id)


def create_tag():
    new_tag = my_db.Tag.objects.create(
        text=fake.word()
    )
    new_tag.save()


def connect_tag():
    # получаем случайный валидный вопрос
    all_question = my_db.Question.objects.all()
    random_question = all_question[random.randint(0, all_question.__len__() - 1)]
    # случайный тег
    all_tag = my_db.Tag.objects.all()
    random_tag = all_tag[random.randint(0, all_tag.__len__() - 1)]

    random_question.tags.add(random_tag)
    random_question.save()
    print("Тег '", random_tag.text, "' добавлен в вопрос ", random_question.id, " получилось ",
          [i.text for i in random_question.tags.all()])


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in range(10):
            create_user()
        for i in range(50):
            create_question()
        for i in range(100):
            create_answer()
        for i in range(10):
            create_question_like()
        for i in range(10):
            create_answer_like()
        for i in range(30):
            create_tag()
        for i in range(10):
            connect_tag()
        pass
