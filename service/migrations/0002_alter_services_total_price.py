# Generated by Django 3.2 on 2021-05-04 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='services',
            name='total_price',
            field=models.FloatField(null=True),
        ),
    ]