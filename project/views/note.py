from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelformset_factory
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from project.models import Note


class NoteListView(ListView):
    model = Note


class NoteDetailView(DetailView):
    model = Note

    # https://docs.djangoproject.com/en/4.0/topics/class-based-views/generic-display/#adding-extra-context
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        fields = self.object._meta.get_fields()
        context["fields"] = fields

        return context


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    fields = ["hours", "date", "timesheet"]


class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    fields = ["hours", "date", "timesheet"]

    def get_success_url(self):
        return reverse("note-detail", kwargs={"pk": self.object.pk})


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    success_url = reverse_lazy("note-list")


@login_required
def manage_notes(request):

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

    NoteFormSet = modelformset_factory(
        Note,
        fields=("hours", "date", "timesheet"),
        can_order=can_order,
        can_delete=can_delete,
        extra=extra,
    )
    if request.method == "POST":
        formset = NoteFormSet(request.POST, request.FILES)
        if formset.is_valid():
            # do something with the formset.cleaned_data
            formset.save()
            return redirect("/")
    else:
        formset = NoteFormSet()

    context["formset"] = formset

    return render(request, "manage_notes.html", context)
