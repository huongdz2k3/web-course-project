# Generated by Django 4.1.6 on 2023-05-06 16:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0028_remove_role_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="course",
            name="author",
        ),
    ]
