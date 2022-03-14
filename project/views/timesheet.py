from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, FormMixin, UpdateView

from project.models import TimeEntry, TimeSheet


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


@login_required
def manage_timesheet(request, pk=None):

    context = {}

    timeentry_extra = request.GET.get("timeentry-extra")
    timeentry_plus = request.GET.get("timeentry-plus")
    timeentry_minus = request.GET.get("timeentry-minus")

    if timeentry_plus:
        timeentry_extra = int(timeentry_extra) + 1
    elif timeentry_minus:
        timeentry_extra = int(timeentry_extra) - 1
    else:
        timeentry_extra = 0

    timeentry_can_delete = True
    timeentry_can_order = False

    context["timeentry_extra"] = timeentry_extra
    context["timeentry_plus"] = timeentry_plus
    context["timeentry_minus"] = timeentry_minus

    timesheet = TimeSheet.objects.get(pk=pk)

    TimeEntryFormSet = inlineformset_factory(
        TimeSheet,
        TimeEntry,
        fields=("hours", "date", "timesheet"),
        can_order=timeentry_can_order,
        can_delete=timeentry_can_delete,
        extra=timeentry_extra,
    )
    if request.method == "POST":
        timeentry_formset = TimeEntryFormSet(request.POST, request.FILES, instance=timesheet)
        if timeentry_formset.is_valid():
            # do something with the formset.cleaned_data
            timeentry_formset.save()
            return redirect("/")
    else:
        timeentry_formset = TimeEntryFormSet(instance=timesheet)

    context["timeentry_formset"] = timeentry_formset
    context["timesheet"] = timesheet

    return render(request, "manage_timesheet.html", context)
