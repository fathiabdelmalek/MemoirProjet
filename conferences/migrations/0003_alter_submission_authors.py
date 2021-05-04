# Generated by Django 3.2 on 2021-05-03 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conferences', '0002_alter_submission_article_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='authors',
            field=models.ManyToManyField(blank=True, null=True, related_name='article_authors', to='conferences.Author'),
        ),
    ]