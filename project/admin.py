from django.contrib import admin

from project.models import TimeEntry, TimeSheet


@admin.register(TimeSheet)
class DocumentAdmin(admin.ModelAdmin):
    """"""


@admin.register(TimeEntry)
class TimeEntryAdmin(admin.ModelAdmin):
    """"""
