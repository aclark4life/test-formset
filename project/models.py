from django.db import models


class TimeEntry(models.Model):
    """ """

    class Meta:
        verbose_name_plural = "Time Entries"

    hours = models.DecimalField(decimal_places=2, max_digits=4, default=1)
