# Generated by Django 4.1.6 on 2023-06-05 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0047_alter_instructor_role_alter_learner_role_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="instructor",
            name="role",
            field=models.CharField(default="1", max_length=10),
        ),
        migrations.AlterField(
            model_name="learner",
            name="role",
            field=models.CharField(default="0", max_length=10),
        ),
        migrations.AlterField(
            model_name="role",
            name="role",
            field=models.CharField(
                choices=[("0", "Learner"), ("1", "Instructor")], max_length=10
            ),
        ),
    ]
