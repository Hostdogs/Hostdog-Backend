# Generated by Django 3.2 on 2021-04-11 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20210411_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='first_name',
            field=models.CharField(default='john', max_length=30),
        ),
        migrations.AddField(
            model_name='customer',
            name='last_name',
            field=models.CharField(default='yeet', max_length=30),
        ),
        migrations.AddField(
            model_name='host',
            name='first_name',
            field=models.CharField(default='john', max_length=30),
        ),
        migrations.AddField(
            model_name='host',
            name='last_name',
            field=models.CharField(default='yeet', max_length=30),
        ),
    ]
