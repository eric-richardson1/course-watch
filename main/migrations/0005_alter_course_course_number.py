# Generated by Django 4.2.3 on 2023-07-24 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_course_course_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_number',
            field=models.FloatField(unique=True),
        ),
    ]
