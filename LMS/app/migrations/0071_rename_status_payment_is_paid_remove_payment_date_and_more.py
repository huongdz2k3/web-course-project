# Generated by Django 4.2.4 on 2023-08-13 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0070_remove_answer_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='status',
            new_name='is_paid',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='date',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='payment_id',
        ),
        migrations.AddField(
            model_name='payment',
            name='address_1',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='payment',
            name='address_2',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='payment',
            name='city',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='payment',
            name='country',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='payment',
            name='email',
            field=models.EmailField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='payment',
            name='order_comments',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='phone',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='payment',
            name='postcode',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='payment',
            name='state',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='payment',
            name='total',
            field=models.IntegerField(default=0),
        ),
    ]