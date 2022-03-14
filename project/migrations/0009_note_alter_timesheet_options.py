# Generated by Django 4.0.3 on 2022-03-14 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0008_rename_document_timesheet_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Note",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.CharField(max_length=2100)),
            ],
        ),
        migrations.AlterModelOptions(
            name="timesheet",
            options={"verbose_name_plural": "Time Sheets"},
        ),
    ]
