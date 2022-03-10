from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.forms import formset_factory
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from project.forms import TimeEntryForm
from project.models import TimeEntry


class TimeEntryListView(ListView):
    model = TimeEntry


class TimeEntryDetailView(DetailView):
    model = TimeEntry

    # https://docs.djangoproject.com/en/4.0/topics/class-based-views/generic-display/#adding-extra-context
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        fields = self.object._meta.get_fields()
        context["fields"] = fields

        return context


class TimeEntryCreateView(LoginRequiredMixin, CreateView):
    model = TimeEntry
    fields = ["hours", "date"]


class TimeEntryUpdateView(LoginRequiredMixin, UpdateView):
    model = TimeEntry
    fields = ["hours", "date"]

    def get_success_url(self):
        return reverse("timeentry-detail", kwargs={"pk": self.object.pk})


class TimeEntryDeleteView(LoginRequiredMixin, DeleteView):
    model = TimeEntry
    success_url = reverse_lazy("timeentry-list")


def manage_timeentries(request):

    context = {}

    extra = request.GET.get("extra")

    if extra:
        extra = int(extra) + 1
    else:
        extra = 1

    context["extra"] = extra

    TimeEntryFormSet = formset_factory(
        TimeEntryForm, can_order=True, can_delete=True, extra=extra
    )
    if request.method == "POST":
        formset = TimeEntryFormSet(request.POST, request.FILES)
        if formset.is_valid():
            # do something with the formset.cleaned_data
            pass
    else:
        formset = TimeEntryFormSet()

    context["formset"] = formset

    return render(request, "manage_timeentries.html", context)
