"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import (
    include,
    path,
    re_path)
from django.views.generic.base import TemplateView


admin.autodiscover()


urlpatterns = [
    re_path(r"^admin/", admin.site.urls),

    re_path(r"^api/", include("api.urls")),
    re_path(r"^", include("app.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
