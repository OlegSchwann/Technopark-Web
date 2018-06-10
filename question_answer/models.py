# Создать модели для основных сущностей: вопрос, ответ, тэг, профиль пользователя, лайк.
# Важно использовать правильные типы данных и проставить необходимые связи (ForeignKey) в моделях.
# Для вопросов создать свой Model Manager, в котором определить выборки “лучшее” и “новое”.
# Как пользоваться полями связи:
#  https://djbook.ru/rel1.7/topics/db/queries.html#saving-foreignkey-and-manytomanyfield-fields
from django.db import models
from django.contrib.auth.models import User
import django.db.models.signals as signals
from django.dispatch import receiver

# замечания по User
# NickName, должен быть уникальным
# User.username
#
# Имя, под которым пользователи видят друг друга.
# Его можно менять
# User.first_name
#
# E-mail
# User.email
#
# Password
# User.password

class Profile(models.Model):
    # ссылка на стандартную форму, с помощью которой происходит авторизация и регистрация
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # ссылка на Аватар
    avatar = models.ImageField(null=True, upload_to='avatars')


# тэг
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

# Сигналы post_save и pre_save НЕ работают! И не дебажатся абсолютно!
# Логика поддержания целостности находится в обработчиках формы.

#  данные для правой колонки (лучшие пользователи, популярные тэги).
#  Популярные тэги - это 10 тэгов с самым большим количеством вопросов за последние 3 месяца.

# тэг --выборка--> popular_tags
class ExcerptTag(models.Model):
    # текст комментария
    text = models.TextField()

#  Лучшие пользователи - это пользователи с самым большим количеством вопросов + ответов за последние 3 месяца.
class ExcerptUsername(models.Model):
    # текст комментария
    username = models.TextField()
