# Generated by Django 4.1.6 on 2023-06-03 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0037_alter_course_certificate"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="featured_image",
            field=models.FileField(null=True, upload_to="Media/featured_img"),
        ),
    ]
