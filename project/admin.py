from django.contrib import admin

from project.models import Note, TimeEntry, TimeSheet


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    """"""


@admin.register(TimeSheet)
class TimeSheetAdmin(admin.ModelAdmin):
    """"""


@admin.register(TimeEntry)
class TimeEntryAdmin(admin.ModelAdmin):
    """"""
