# Generated by Django 4.0.3 on 2022-03-16 17:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0015_course_timesheet"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="course",
            name="end",
        ),
        migrations.RemoveField(
            model_name="course",
            name="start",
        ),
        migrations.RemoveField(
            model_name="course",
            name="title",
        ),
    ]
