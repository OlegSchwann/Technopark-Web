import question_answer.models as models
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta

# этот инструмент пересчитывает лучших пользователей -
# это пользователи с самым большим количеством вопросов + ответов за последнюю неделю.
class Command(BaseCommand):
    def handle(self, *args, **options):
        week_before = datetime.now() - timedelta(weeks=1)
        user_counter = {}
        for user in models.User.objects.all():
            question_count = user.profile.question_set.filter(time__gte=week_before).count()
            answer_count = user.profile.answer_set.filter(time__gte=week_before).count()
            user_counter[user.username] = question_count + answer_count

        # https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary#12343826
        result = []
        values = list(user_counter.values())
        keys = list(user_counter.keys())
        for i in range(10):
            max_index = values.index(max(values))
            result.append(keys[max_index])
            values[max_index] = -1  # исключаем значение, так как все остальные точно положительные.

        # вставляем полученные значения обратно в таблицу
        models.ExcerptUsername.objects.all().delete()
        for username in result:
            models.ExcerptUsername.objects.create(username=username).save()
