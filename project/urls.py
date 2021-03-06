from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import include, path
from django.views.i18n import JavaScriptCatalog
from rest_framework import routers, serializers, viewsets
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from project.views import timeentry as timeentry_views
from project.views import timesheet as timesheet_views
from project.views.timeentry import (
    TimeEntryCreateView,
    TimeEntryDeleteView,
    TimeEntryUpdateView,
)
from project.views.timesheet import (
    TimeSheetCreateView,
    TimeSheetDeleteView,
    TimeSheetUpdateView,
)
from search import views as search_views

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("wagtail-documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # debug toolbar
    urlpatterns = urlpatterns + [
        path("__debug__/", include("debug_toolbar.urls")),
    ]

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
        "timeentries/",
        timeentry_views.TimeEntryListView.as_view(),
        name="timeentry-list",
    ),
    path(
        "timeentries/<int:pk>/detail/",
        timeentry_views.TimeEntryDetailView.as_view(),
        name="timeentry-detail",
    ),
    path("timeentries/add/", TimeEntryCreateView.as_view(), name="timeentry-add"),
    path(
        "timeentries/<int:pk>/", TimeEntryUpdateView.as_view(), name="timeentry-update"
    ),
    path(
        "timeentries/<int:pk>/delete/",
        TimeEntryDeleteView.as_view(),
        name="timeentry-delete",
    ),
    path(
        "timeentries/manage/",
        timeentry_views.manage_timeentries,
        name="timeentry-manage",
    ),
]


urlpatterns = urlpatterns + [
    path(
        "timesheets/",
        timesheet_views.TimeSheetListView.as_view(),
        name="timesheet-list",
    ),
    path(
        "timesheets/<int:pk>/detail/",
        timesheet_views.TimeSheetDetailView.as_view(),
        name="timesheet-detail",
    ),
    path("timesheets/add/", TimeSheetCreateView.as_view(), name="timesheet-add"),
    path(
        "timesheets/<int:pk>/", TimeSheetUpdateView.as_view(), name="timesheet-update"
    ),
    path(
        "timesheets/<int:pk>/delete/",
        TimeSheetDeleteView.as_view(),
        name="timesheet-delete",
    ),
    path(
        "timesheets/<int:pk>/manage/",
        timesheet_views.manage_timesheet,
        name="timesheet-manage",
    ),
]

urlpatterns = urlpatterns + [
    path("jsi18n/", JavaScriptCatalog.as_view(), name="jsi18n"),
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
