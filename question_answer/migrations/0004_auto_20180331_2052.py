# Generated by Django 2.0.2 on 2018-03-31 20:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('question_answer', '0003_auto_20180331_0742'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answerlike',
            old_name='user_id',
            new_name='profile_id',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='user_id',
            new_name='profile_id',
        ),
        migrations.RenameField(
            model_name='questionlike',
            old_name='user_id',
            new_name='profile_id',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='user_id',
        ),
        migrations.AddField(
            model_name='answer',
            name='profile_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='question_answer.Profile'),
        ),
    ]
