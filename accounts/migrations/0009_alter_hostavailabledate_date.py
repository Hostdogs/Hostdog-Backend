# Generated by Django 3.2 on 2021-05-02 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20210501_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostavailabledate',
            name='date',
            field=models.DateField(),
        ),
    ]