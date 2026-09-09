from django.apps import apps
from django.contrib import admin
from django.contrib.auth.decorators import login_required as auth
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic.base import TemplateView


admin.site.site_header = settings.APPLICATION_NAME
admin.site.site_title = settings.APPLICATION_NAME

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", auth(TemplateView.as_view(template_name="home.html")), name="home"),
    path("", include("core.urls")),
    path("reports/", include(("reports.urls", "reports"))),
    path("scorecard/", include(("scorecard.urls", "scorecard"))),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    if apps.is_installed("django_browser_reload"):
        urlpatterns += [path("__reload__/", include("django_browser_reload.urls"))]
