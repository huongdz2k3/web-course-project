# Generated by Django 4.2.4 on 2023-08-11 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0067_alter_learner_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructor',
            name='phone',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
