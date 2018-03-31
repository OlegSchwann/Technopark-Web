from django.core.management.base import BaseCommand
import question_answer.models as my_db

class Command(BaseCommand):
    def handle(self, *args, **options):
        one_user = my_db.User.objects.create_user(
            username='1st-user',
            email='Max@askmax.io',
            password="12345678"
        )
        one_user.profile.avatar_link = 'http://localhost:8080/static/1st-user.jpeg'
        one_user.save()
        print("one_user.id = ", one_user.id)
