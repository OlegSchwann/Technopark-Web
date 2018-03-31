# Создать модели для основных сущностей: вопрос, ответ, тэг, профиль пользователя, лайк.
# Важно использовать правильные типы данных и проставить необходимые связи (ForeignKey) в моделях.
# Для вопросов создать свой Model Manager, в котором определить выборки “лучшее” и “новое”.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    # использование one two one field слишком сложно.
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

# вопрос
class Question(models.Model):
    # id первичный ключ
    id = models.AutoField(primary_key=True)
    # заголовок
    title = models.TextField()
    # непосредственно текст вопроса
    text = models.TextField()
    # внешний ключ пользователя, задавшего вопрос
    user_id = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL)
    # время вопроса
    time = models.DateTimeField()


# тэг --выборка--> popular_tags
class Tag(models.Model):
    # id первичный ключ
    id = models.AutoField(primary_key=True)
    # текст комментария
    text = models.TextField()


# таблица связи между тегами и вопросами
class QuestionTag(models.Model):
    # id первичный ключ
    id = models.AutoField(primary_key=True)
    # id вопроса
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    # id тега
    tad_id = models.ForeignKey(Tag, on_delete=models.CASCADE)


# ответ
class Answer(models.Model):
    # id первичный ключ
    id = models.AutoField(primary_key=True)
    # непосредственно текст ответа
    text = models.TextField()
    # внешний ключ ответившего пользователя
    user_id = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    # внешний ключ вопроса
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    # время ответа
    time = models.DateTimeField()
    # флаг лучшего ответа, ответ отображается первым, если есть. Может поставить только автор вопроса
    best_ansver = models.BooleanField()


# лайк для вопросов
class QuestionLike(models.Model):
    # id первичный ключ
    id = models.AutoField(primary_key=True)
    # id пользователя, поставившего оценку, index
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    # id оцененного ответа, index
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    # присвоенный статус: boolean: true == '+', false == '-'
    status = models.BooleanField()


# лайк для ответов
class AnswerLike(models.Model):
    # id первичный ключ
    id = models.AutoField(primary_key=True)
    # id пользователя, поставившего оценку, index
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    # id оцененного ответа, index
    question_id = models.ForeignKey(Answer, on_delete=models.CASCADE)
    # присвоенный статус: boolean: true == '+', false == '-'
    status = models.BooleanField()
