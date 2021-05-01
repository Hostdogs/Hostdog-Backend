# Generated by Django 3.2 on 2021-05-01 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_dog_dog_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=22, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=22, null=True),
        ),
        migrations.AlterField(
            model_name='host',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=22, null=True),
        ),
        migrations.AlterField(
            model_name='host',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=22, null=True),
        ),
    ]