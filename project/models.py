from django.db import models
from django.utils import timezone


class TimeEntry(models.Model):
    class Meta:
        verbose_name_plural = "Time Entries"

    hours = models.DecimalField(decimal_places=2, max_digits=4, default=1)
    date = models.DateField(default=timezone.now)
