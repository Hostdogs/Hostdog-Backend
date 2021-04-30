# Generated by Django 3.2 on 2021-04-30 14:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0014_auto_20210430_2110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='services',
            name='service_meal_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='service_meal_type', to='service.meal'),
        ),
    ]