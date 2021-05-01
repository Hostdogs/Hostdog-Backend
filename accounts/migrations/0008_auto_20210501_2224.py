# Generated by Django 3.2 on 2021-05-01 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20210501_2219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=20, max_digits=32, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=20, max_digits=32, null=True),
        ),
        migrations.AlterField(
            model_name='host',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=20, max_digits=32, null=True),
        ),
        migrations.AlterField(
            model_name='host',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=20, max_digits=32, null=True),
        ),
    ]