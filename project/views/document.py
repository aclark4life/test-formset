from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.forms import modelformset_factory
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from project.models import Document


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
    fields = ["hours", "date"]


class DocumentUpdateView(LoginRequiredMixin, UpdateView):
    model = Document
    fields = ["hours", "date"]

    def get_success_url(self):
        return reverse("document-detail", kwargs={"pk": self.object.pk})


class DocumentDeleteView(LoginRequiredMixin, DeleteView):
    model = Document
    success_url = reverse_lazy("document-list")


def manage_documents(request):

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

    DocumentFormSet = modelformset_factory(
        Document,
        fields=("hours", "date"),
        can_order=can_order,
        can_delete=can_delete,
        extra=extra,
    )
    if request.method == "POST":
        formset = DocumentFormSet(request.POST, request.FILES)
        if formset.is_valid():
            # do something with the formset.cleaned_data
            formset.save()
            return redirect("/")
    else:
        formset = DocumentFormSet()

    context["formset"] = formset

    return render(request, "manage_documents.html", context)
