# Generated by Django 3.2 on 2021-04-10 15:45

import datetime
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_host', models.BooleanField(default=False)),
                ('is_customer', models.BooleanField(default=False)),
                ('address', models.CharField(blank=True, max_length=255)),
                ('mobile', models.CharField(blank=True, max_length=10)),
                ('dob', models.DateField(default=datetime.date(2021, 4, 10))),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='accounts.accounts')),
                ('customer_bio', models.TextField(blank=True, max_length=100)),
                ('customer_dog_count', models.IntegerField(default=0)),
                ('customer_hosted_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='accounts.accounts')),
                ('host_bio', models.TextField(blank=True, max_length=100)),
                ('host_rating', models.FloatField(default=0.0)),
                ('host_hosted_count', models.IntegerField(default=0)),
                ('host_max', models.IntegerField(default=0)),
                ('host_avaliable', models.IntegerField(default=0)),
                ('host_area', models.FloatField(default=0.0)),
                ('host_schedule', models.TextField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Dog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dog_name', models.CharField(max_length=50)),
                ('dog_bio', models.TextField(max_length=100)),
                ('dog_status', models.CharField(max_length=20)),
                ('dog_create_date', models.DateField(auto_now_add=True)),
                ('dog_dob', models.DateField(default=datetime.date(2021, 4, 10))),
                ('dog_breed', models.CharField(max_length=20)),
                ('dog_weight', models.FloatField(default=0.0)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.customer')),
            ],
        ),
    ]
