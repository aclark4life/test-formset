from django.core import serializers
from django.urls import reverse_lazy
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

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
        return reverse("user-detail", kwargs={"pk": self.object.pk})


class TimeEntryDeleteView(LoginRequiredMixin, DeleteView):
    model = TimeEntry
    success_url = reverse_lazy("user-list")
