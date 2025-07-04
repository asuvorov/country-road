"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

from django.urls import (
    include,
    re_path)

from . import views


urlpatterns = [
    re_path(r"^agencies/stats/$", views.api_agency_stats, name="api-agency-stats"),
    re_path(r"^titles/stats/$", views.api_title_stats, name="api-title-stats"),
]
