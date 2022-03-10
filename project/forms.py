from django import forms

from project.models import TimeEntry


class TimeEntryForm(forms.ModelForm):
    """"""

    class Meta:
        model = TimeEntry
        fields = ["hours", "date"]
