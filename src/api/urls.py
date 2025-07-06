"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

from django.urls import (
    include,
    re_path)


urlpatterns = [
    re_path(r"^v1/", include("api.v1.urls")),
]
