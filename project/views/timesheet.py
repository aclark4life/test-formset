from crispy_forms.helper import FormHelper
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, FormMixin, UpdateView

from project.models import Course, Note, TimeEntry, TimeSheet


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


class TimeEntryFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_tag = False


class NoteFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_tag = False


class CourseFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_tag = False
        self.include_media = True


@login_required
def manage_timesheet(request, pk=None):

    context = {}

    course_extra = request.GET.get("course-extra")
    course_plus = request.GET.get("course-plus")
    course_minus = request.GET.get("course-minus")
    note_extra = request.GET.get("note-extra")
    note_plus = request.GET.get("note-plus")
    note_minus = request.GET.get("note-minus")
    timeentry_extra = request.GET.get("timeentry-extra")
    timeentry_plus = request.GET.get("timeentry-plus")
    timeentry_minus = request.GET.get("timeentry-minus")

    if timeentry_plus:
        timeentry_extra = int(timeentry_extra) + 1
        note_extra = int(note_extra)
        course_extra = int(course_extra)
    elif timeentry_minus:
        timeentry_extra = int(timeentry_extra) - 1
        note_extra = int(note_extra)
        course_extra = int(course_extra)
    elif note_plus:
        timeentry_extra = int(timeentry_extra)
        note_extra = int(note_extra) + 1
        course_extra = int(course_extra)
    elif note_minus:
        timeentry_extra = int(timeentry_extra)
        note_extra = int(note_extra) - 1
        course_extra = int(course_extra)
    elif course_plus:
        timeentry_extra = int(timeentry_extra)
        note_extra = int(note_extra)
        course_extra = int(course_extra) + 1
    elif course_minus:
        timeentry_extra = int(timeentry_extra)
        note_extra = int(note_extra)
        course_extra = int(course_extra) - 1
    else:
        timeentry_extra = note_extra = course_extra = 0

    timeentry_can_delete = True
    timeentry_can_order = False
    note_can_delete = True
    note_can_order = False
    course_can_delete = True
    course_can_order = False

    context["timeentry_extra"] = timeentry_extra
    context["timeentry_plus"] = timeentry_plus
    context["timeentry_minus"] = timeentry_minus
    context["note_extra"] = note_extra
    context["note_plus"] = note_plus
    context["note_minus"] = note_minus
    context["course_extra"] = course_extra
    context["course_plus"] = course_plus
    context["course_minus"] = course_minus

    timesheet = TimeSheet.objects.get(pk=pk)

    TimeEntryFormSet = inlineformset_factory(
        TimeSheet,
        TimeEntry,
        fields=("hours", "date", "timesheet"),
        can_order=timeentry_can_order,
        can_delete=timeentry_can_delete,
        extra=timeentry_extra,
    )

    NoteFormSet = inlineformset_factory(
        TimeSheet,
        Note,
        fields=("text", "timesheet"),
        can_order=note_can_order,
        can_delete=note_can_delete,
        extra=note_extra,
    )

    CourseFormSet = inlineformset_factory(
        TimeSheet,
        Course,
        fields=("recurrences", "timesheet"),
        can_order=course_can_order,
        can_delete=course_can_delete,
        extra=course_extra,
    )

    formset_helper_timeentry = TimeEntryFormSetHelper()
    formset_helper_note = NoteFormSetHelper()
    formset_helper_course = CourseFormSetHelper()

    if request.method == "POST":
        timeentry_formset = TimeEntryFormSet(
            request.POST, request.FILES, instance=timesheet, prefix="timeentry"
        )

        note_formset = NoteFormSet(
            request.POST, request.FILES, instance=timesheet, prefix="note"
        )

        course_formset = CourseFormSet(
            request.POST, request.FILES, instance=timesheet, prefix="course"
        )

        if (
            timeentry_formset.is_valid()
            and note_formset.is_valid()
            and course_formset.is_valid()
        ):
            timeentry_formset.save()
            note_formset.save()
            course_formset.save()
            return redirect(reverse("timesheet-detail", kwargs={"pk": pk}))
    else:
        timeentry_formset = TimeEntryFormSet(instance=timesheet, prefix="timeentry")
        note_formset = NoteFormSet(instance=timesheet, prefix="note")
        course_formset = CourseFormSet(instance=timesheet, prefix="course")

    context["timeentry_formset"] = timeentry_formset
    context["note_formset"] = note_formset
    context["course_formset"] = course_formset
    context["timesheet"] = timesheet
    context["formset_helper_timeentry"] = formset_helper_timeentry
    context["formset_helper_note"] = formset_helper_note
    context["formset_helper_course"] = formset_helper_course

    return render(request, "manage_timesheet.html", context)
