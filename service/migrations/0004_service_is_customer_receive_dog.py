# Generated by Django 3.2 on 2021-04-27 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_auto_20210428_0041'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='is_customer_receive_dog',
            field=models.BooleanField(default=False),
        ),
    ]
