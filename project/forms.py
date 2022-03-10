from django import forms
from django.forms import formset_factory


class TimeEntryForm(forms.Form):
    """"""


TimeEntryFormSet = formset_factory(TimeEntryForm)
