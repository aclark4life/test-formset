from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.forms import inlineformset_factory, modelformset_factory
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


def manage_documents(request):

    context = {}

    TimeEntryFormSet = inlineformset_factory(
        Document,
        TimeEntry,
        fields=[
            "document",
        ],
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

    return render(request, "manage_documents.html", context)
