# Generated by Django 3.2 on 2021-04-28 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210426_2151'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounts',
            name='account_number',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]