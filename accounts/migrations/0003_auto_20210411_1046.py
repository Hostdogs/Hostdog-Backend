# Generated by Django 3.2 on 2021-04-11 03:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_accounts_is_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accounts',
            name='address',
        ),
        migrations.RemoveField(
            model_name='accounts',
            name='dob',
        ),
        migrations.RemoveField(
            model_name='accounts',
            name='mobile',
        ),
        migrations.AddField(
            model_name='customer',
            name='address',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='customer',
            name='dob',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='customer',
            name='mobile',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='host',
            name='address',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='host',
            name='dob',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='host',
            name='mobile',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
