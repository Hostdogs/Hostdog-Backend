# Generated by Django 3.2 on 2021-04-18 16:13

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_customer_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog',
            name='picture',
            field=models.ImageField(blank=True, upload_to=accounts.models.Dog.path_and_rename, verbose_name="Dog's image"),
        ),
        migrations.AlterField(
            model_name='host',
            name='picture',
            field=models.ImageField(blank=True, upload_to=accounts.models.Host.path_and_rename, verbose_name="Host's image"),
        ),
    ]
