from django.contrib import admin

from project.models import TimeEntry
from project.models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """"""


@admin.register(TimeEntry)
class TimeEntryAdmin(admin.ModelAdmin):
    """"""
