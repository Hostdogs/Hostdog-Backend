# Generated by Django 3.2 on 2021-04-26 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('none', 'None')], default='Male', max_length=10),
        ),
        migrations.AlterField(
            model_name='host',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('none', 'None')], default='Male', max_length=10),
        ),
    ]