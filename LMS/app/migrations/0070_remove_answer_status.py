# Generated by Django 4.2.4 on 2023-08-12 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0069_answer_status_question_status_alter_question_point'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='status',
        ),
    ]