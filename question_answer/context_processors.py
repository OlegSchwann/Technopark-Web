import question_answer.models as models


# этот файл содержит контекстные процессоры:
# https://docs.djangoproject.com/en/2.0/ref/templates/api/#writing-your-own-context-processors
# https://www.webforefront.com/django/setupdjangocontextprocessors.html

# достаёт популярные теги из кеша
def extract_top_tag(request):
    return {
        "excerpt_tags": [i.text for i in models.ExcerptTag.objects.all()]
    }


# и достаёт самых активных пользователей из кеша
def extract_top_users(request):
    return {
        "excerpt_usernames": [i.username for i in models.ExcerptUsername.objects.all()]
    }
