# Generated by Django 4.2.3 on 2023-07-24 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='watched_courses',
            field=models.ManyToManyField(to='main.course'),
        ),
    ]
