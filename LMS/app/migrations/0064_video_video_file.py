# Generated by Django 4.2.3 on 2023-07-23 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0063_course_course_type_alter_video_youtube_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="video",
            name="video_file",
            field=models.FileField(null=True, upload_to="ProtectedVideoLectures"),
        ),
    ]