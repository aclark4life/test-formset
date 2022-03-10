from django.contrib import admin

from project.models import TimeEntry


class TimeEntryAdmin(admin.ModelAdmin):
    """"""


admin.site.register(TimeEntry, TimeEntryAdmin)
