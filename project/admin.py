from django.contrib import admin

from project.models import TimeSheet, TimeEntry


@admin.register(TimeSheet)
class DocumentAdmin(admin.ModelAdmin):
    """"""


@admin.register(TimeEntry)
class TimeEntryAdmin(admin.ModelAdmin):
    """"""
