# Generated by Django 3.2 on 2021-04-23 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('read', models.BooleanField(default=False)),
                ('received_date', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications_customer', to='accounts.customer')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications_host', to='accounts.host')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification_service', to='service.service')),
            ],
        ),
    ]
