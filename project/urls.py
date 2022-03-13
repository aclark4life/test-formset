from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import include, path
from rest_framework import routers, serializers, viewsets
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from project import views as project_views
from project.views import TimeEntryCreateView, TimeEntryDeleteView, TimeEntryUpdateView
from project.views import document as document_views
from project.views.document import (
    DocumentCreateView,
    DocumentDeleteView,
    DocumentUpdateView,
)
from search import views as search_views

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# https://www.django-rest-framework.org/#example
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "is_staff"]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


router = routers.DefaultRouter()
router.register(r"users", UserViewSet)

urlpatterns = urlpatterns + [
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]


urlpatterns = urlpatterns + [
    path(
        "time-entries/",
        project_views.TimeEntryListView.as_view(),
        name="timeentry-list",
    ),
    path(
        "time-entries/<int:pk>/detail/",
        project_views.TimeEntryDetailView.as_view(),
        name="timeentry-detail",
    ),
    path("time-entries/add/", TimeEntryCreateView.as_view(), name="timeentry-add"),
    path(
        "time-entries/<int:pk>/", TimeEntryUpdateView.as_view(), name="timeentry-update"
    ),
    path(
        "time-entries/<int:pk>/delete/",
        TimeEntryDeleteView.as_view(),
        name="timeentry-delete",
    ),
    path(
        "time-entries/manage/",
        project_views.manage_timeentries,
        name="timeentry-manage",
    ),
]


urlpatterns = urlpatterns + [
    path(
        "documents/",
        document_views.DocumentListView.as_view(),
        name="document-list",
    ),
    path(
        "documents/<int:pk>/detail/",
        document_views.DocumentDetailView.as_view(),
        name="document-detail",
    ),
    path("documents/add/", DocumentCreateView.as_view(), name="document-add"),
    path("documents/<int:pk>/", DocumentUpdateView.as_view(), name="document-update"),
    path(
        "documents/<int:pk>/delete/",
        DocumentDeleteView.as_view(),
        name="document-delete",
    ),
    path(
        "documents/manage/",
        document_views.manage_documents,
        name="document-manage",
    ),
]


urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
