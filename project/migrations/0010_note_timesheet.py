# Generated by Django 4.0.3 on 2022-03-14 18:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0009_note_alter_timesheet_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="note",
            name="timesheet",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="project.timesheet",
            ),
        ),
    ]
