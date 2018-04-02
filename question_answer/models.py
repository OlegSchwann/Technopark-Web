# Создать модели для основных сущностей: вопрос, ответ, тэг, профиль пользователя, лайк.
# Важно использовать правильные типы данных и проставить необходимые связи (ForeignKey) в моделях.
# Для вопросов создать свой Model Manager, в котором определить выборки “лучшее” и “новое”.
# Как пользоваться полями связи:
#  https://djbook.ru/rel1.7/topics/db/queries.html#saving-foreignkey-and-manytomanyfield-fields
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


class Profile(models.Model):
    # ссылка на стандартную форму, с помощью которой происходит авторизация и регистрация
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # ссылка на Аватар
    avatar_link = models.URLField()
    # avatar = models.ImageField()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# тэг --выборка--> popular_tags
class Tag(models.Model):
    # текст комментария
    text = models.TextField()


# вопрос
class Question(models.Model):
    # id первичный ключ
    id = models.AutoField(primary_key=True)
    # заголовок
    title = models.TextField()
    # непосредственно текст вопроса
    text = models.TextField()
    # внешний ключ пользователя, задавшего вопрос
    profile_id = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL)
    # время вопроса
    time = models.DateTimeField()
    # Для хранения + и - необходима отдельная сущность, QuestionLike.
    # Для того, что бы не создавать нагрузку на базу, храним данные в денормализованном виде,
    # параллельно у Question будет столбец raiting с заранее посчитанным рейтингом.
    # При сбое или сильном изменении за короткое время данные будут рассинхронизированны.
    # Но это оптимальный по производительности вариант.
    rating = models.IntegerField(default=0)
    # ссылки на теги
    tags = models.ManyToManyField(Tag)

# ответ
class Answer(models.Model):
    # id первичный ключ
    id = models.AutoField(primary_key=True)
    # непосредственно текст ответа
    text = models.TextField()
    # внешний ключ ответившего пользователя
    profile_id = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL)
    # внешний ключ вопроса
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    # время ответа
    time = models.DateTimeField()
    # флаг лучшего ответа, ответ отображается первым, если есть. Может поставить только автор вопроса
    best_answer = models.BooleanField()
    # рейтинг вопроса
    rating = models.IntegerField(default=0)


# лайк для вопросов
class QuestionLike(models.Model):
    # id первичный ключ
    id = models.AutoField(primary_key=True)
    # id пользователя, поставившего оценку, index
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    # id оцененного ответа, index
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    # присвоенный статус: int: 1 == '+', -1 == '-'
    status = models.IntegerField(default=0)


@receiver(post_save, sender=QuestionLike)
def create_question_like(instance, created, **kwargs):
    """Callback, which add which reflects the rating in Question on every new QuestionLike"""
    updated_question = instance.question_id
    print("добавляется ", instance.status, ", старый рейтинг ", updated_question.rating)
    updated_question.rating += instance.status
    updated_question.save()
    print("новый рейтинг", updated_question.rating)


# @receiver(pre_delete, sender=QuestionLike)
# def delete_user_profile(instance, **kwargs):
#     """Callback, which add which reflects the rating in Question on every new QuestionLike"""
#     updated_question = instance.question_id
#     updated_question.rating -= instance.status
#     updated_question.save()


# лайк для ответов
class AnswerLike(models.Model):
    # id первичный ключ
    id = models.AutoField(primary_key=True)
    # id пользователя, поставившего оценку, index
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    # id оцененного ответа, index
    answer_id = models.ForeignKey(Answer, on_delete=models.CASCADE)
    # присвоенный статус: int: 1 == '+', -1 == '-'
    status = models.IntegerField(default=0)


@receiver(post_save, sender=AnswerLike)
def create_user_profile(instance, created, **kwargs):
    if created:
        updated_answer = instance.answer_id
        updated_answer.rating += instance.status
        updated_answer.save()

# @receiver(pre_delete, sender=AnswerLike)
# def create_user_profile(instance, created, **kwargs):
#     if created:
#         updated_answer = instance.answer_id
#         updated_answer.rating -= instance.status
#         updated_answer.save()
