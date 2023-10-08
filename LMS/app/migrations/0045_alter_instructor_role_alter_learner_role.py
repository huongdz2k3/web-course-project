# Generated by Django 4.1.6 on 2023-06-04 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0044_alter_learner_role"),
    ]

    operations = [
        migrations.AlterField(
            model_name="instructor",
            name="role",
            field=models.ForeignKey(
                default="1", on_delete=django.db.models.deletion.CASCADE, to="app.role"
            ),
        ),
        migrations.AlterField(
            model_name="learner",
            name="role",
            field=models.ForeignKey(
                default="0", on_delete=django.db.models.deletion.CASCADE, to="app.role"
            ),
        ),
    ]