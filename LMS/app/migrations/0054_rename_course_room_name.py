# Generated by Django 4.2.3 on 2023-07-15 13:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0053_room_message"),
    ]

    operations = [
        migrations.RenameField(
            model_name="room",
            old_name="course",
            new_name="name",
        ),
    ]
