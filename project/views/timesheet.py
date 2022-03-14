from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, FormMixin, UpdateView

from project.models import TimeSheet, TimeEntry


class TimeSheetListView(ListView):
    model = TimeSheet


class TimeSheetDetailView(DetailView):
    model = TimeSheet

    # https://docs.djangoproject.com/en/4.0/topics/class-based-views/generic-display/#adding-extra-context
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        fields = self.object._meta.get_fields()
        context["fields"] = fields

        return context


class TimeSheetCreateView(LoginRequiredMixin, CreateView):
    model = TimeSheet
    fields = "__all__"


class TimeSheetUpdateView(LoginRequiredMixin, UpdateView, FormMixin):
    model = TimeSheet
    fields = "__all__"

    def get_success_url(self):
        return reverse("timesheet-detail", kwargs={"pk": self.object.pk})


class TimeSheetDeleteView(LoginRequiredMixin, DeleteView):
    model = TimeSheet
    success_url = reverse_lazy("timesheet-list")


def manage_timesheet(request, pk=None):

    context = {}

    extra = request.GET.get("extra")
    plus = request.GET.get("plus")
    minus = request.GET.get("minus")

    if plus:
        extra = int(extra) + 1
    elif minus:
        extra = int(extra) - 1
    else:
        extra = 0

    can_delete = True
    can_order = False

    context["extra"] = extra
    context["plus"] = plus
    context["minus"] = minus

    timesheet = TimeSheet.objects.get(pk=pk)

    TimeEntryFormSet = inlineformset_factory(
        TimeSheet,
        TimeEntry,
        fields=("hours", "date", "timesheet"),
        can_order=can_order,
        can_delete=can_delete,
        extra=extra,
    )
    if request.method == "POST":
        formset = TimeEntryFormSet(request.POST, request.FILES, instance=timesheet)
        if formset.is_valid():
            # do something with the formset.cleaned_data
            formset.save()
            return redirect("/")
    else:
        formset = TimeEntryFormSet(instance=timesheet)

    context["formset"] = formset
    context["timesheet"] = timesheet

    return render(request, "manage_timesheet.html", context)
