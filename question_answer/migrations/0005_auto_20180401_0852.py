# Generated by Django 2.0.2 on 2018-04-01 08:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('question_answer', '0004_auto_20180331_2052'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answerlike',
            old_name='question_id',
            new_name='answer_id',
        ),
    ]
