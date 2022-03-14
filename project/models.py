from django.db import models
from django.utils import timezone


class Note(models.Model):
    text = models.CharField(max_length=2100)
    timesheet = models.ForeignKey("TimeSheet", on_delete=models.SET_NULL, null=True)


class TimeSheet(models.Model):
    class Meta:
        verbose_name_plural = "Time Sheets"


class TimeEntry(models.Model):
    class Meta:
        verbose_name_plural = "Time Entries"

    hours = models.DecimalField(decimal_places=2, max_digits=4, default=1)
    date = models.DateField(default=timezone.now)
    timesheet = models.ForeignKey("TimeSheet", on_delete=models.SET_NULL, null=True)
