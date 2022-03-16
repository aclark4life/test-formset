from django.contrib import admin

from project.models import Course, Note, TimeEntry, TimeSheet

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """"""

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    """"""


@admin.register(TimeSheet)
class TimeSheetAdmin(admin.ModelAdmin):
    """"""


@admin.register(TimeEntry)
class TimeEntryAdmin(admin.ModelAdmin):
    """"""
