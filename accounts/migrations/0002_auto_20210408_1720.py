# Generated by Django 3.2 on 2021-04-08 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accounts',
            old_name='firstname',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='accounts',
            old_name='username',
            new_name='user_name',
        ),
    ]