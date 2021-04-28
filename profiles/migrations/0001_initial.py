# Generated by Django 3.2 on 2021-04-28 15:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='birth date')),
                ('sexe', models.IntegerField(blank=True, choices=[(1, 'MALE'), (2, 'FEMALE')], null=True)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('work_place', models.CharField(blank=True, max_length=30, null=True)),
                ('degree', models.IntegerField(blank=True, choices=[(0, 'Student'), (1, 'MBB'), (2, 'MBA'), (3, 'MAB'), (4, 'MAA'), (5, 'Professor')], null=True)),
                ('speciality', models.CharField(blank=True, max_length=50, null=True)),
                ('web_site', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
