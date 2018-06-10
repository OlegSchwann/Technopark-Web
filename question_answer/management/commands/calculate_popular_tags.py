import question_answer.models as models
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta

# этот инструмент пересчитывает популярные теги -
# это 10 тэгов с самым большим количеством вопросов за последнюю неделю
class Command(BaseCommand):
    def handle(self, *args, **options):
        week_before = datetime.now() - timedelta(weeks=1)
        tags_counter = {}
        for question in models.Question.objects.filter(time__gte=week_before).all():
            for tag in question.tags.all():
                tags_counter[tag.text] = tags_counter.get(tag.text, 0) + 1

        # https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary#12343826
        result = []
        values = list(tags_counter.values())
        keys = list(tags_counter.keys())
        for i in range(10):
            max_index = values.index(max(values))
            result.append(keys[max_index])
            values[max_index] = -1  # исключаем значение, так как все остальные точно положительные.

        # вставляем полученные значения обратно в таблицу
        models.ExcerptTag.objects.all().delete()
        for text in result:
            models.ExcerptTag.objects.create(text=text).save()
