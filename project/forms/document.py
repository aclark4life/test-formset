from django import forms
from project.models import Document
from project.models import TimeEntry


class DocumentForm(forms.ModelForm):
    """"""

    class Meta:
        model = Document
        fields = "__all__"

    time_entry = forms.ModelChoiceField(
        queryset=TimeEntry.objects.all(), widget=forms.SelectMultiple
    )
