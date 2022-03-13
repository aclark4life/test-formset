from django.contrib import admin

from project.models import Document, TimeEntry


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """"""


@admin.register(TimeEntry)
class TimeEntryAdmin(admin.ModelAdmin):
    """"""
