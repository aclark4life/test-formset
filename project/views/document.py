from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.forms import inlineformset_factory
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, FormMixin, UpdateView

from project.models import Document, TimeEntry


class DocumentListView(ListView):
    model = Document


class DocumentDetailView(DetailView):
    model = Document

    # https://docs.djangoproject.com/en/4.0/topics/class-based-views/generic-display/#adding-extra-context
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        fields = self.object._meta.get_fields()
        context["fields"] = fields

        return context


class DocumentCreateView(LoginRequiredMixin, CreateView):
    model = Document
    fields = "__all__"


class DocumentUpdateView(LoginRequiredMixin, UpdateView, FormMixin):
    model = Document
    fields = "__all__"

    def get_success_url(self):
        return reverse("document-detail", kwargs={"pk": self.object.pk})


class DocumentDeleteView(LoginRequiredMixin, DeleteView):
    model = Document
    success_url = reverse_lazy("document-list")


def manage_document(request, pk=None):

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

    can_delete = False
    can_order = False

    context["extra"] = extra
    context["plus"] = plus
    context["minus"] = minus

    document = Document.objects.get(pk=pk)

    TimeEntryFormSet = inlineformset_factory(
        Document,
        TimeEntry,
        fields=("hours", "date", "document"),
        can_order=can_order,
        can_delete=can_delete,
        extra=extra,
    )
    if request.method == "POST":
        formset = TimeEntryFormSet(request.POST, request.FILES)
        if formset.is_valid():
            # do something with the formset.cleaned_data
            formset.save()
            return redirect("/")
    else:
        formset = TimeEntryFormSet()

    context["formset"] = formset
    context["document"] = document

    return render(request, "manage_document.html", context)
