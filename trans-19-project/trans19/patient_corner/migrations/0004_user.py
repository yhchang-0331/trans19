# Generated by Django 3.0.4 on 2020-05-14 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_corner', '0003_auto_20200424_0946'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('is_epidemiologist', models.BooleanField(default=False)),
                ('email', models.EmailField(max_length=30, unique=True, verbose_name='email')),
                ('username', models.CharField(max_length=20, unique=True, verbose_name='username')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
