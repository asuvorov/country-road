"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

from django.contrib import admin

from .models import ECFRNode


# =============================================================================
# ===
# === ECFR NODE ADMIN
# ===
# =============================================================================
@admin.register(ECFRNode)
class ECFRNodeAdmin(admin.ModelAdmin):
    """eCFR Node Admin."""

    fieldsets = (
        ("", {
            "classes":  (""),
            "fields":   (
                "path",
            ),
        }),
        ("Significant Labels", {
            "classes":  (
                "grp-collapse grp-closed",
            ),
            "fields":   (
                ("label_type", "identifier"),
                "label",
                "label_level",
                "label_description",
            ),
        }),
        ("Flags", {
            "classes":  (
                "grp-collapse grp-closed",
            ),
            "fields":   (
                "has_children",
            ),
        }),
        ("Content", {
            "classes":  (""),
            "fields":   (
                "content",
            ),
        }),
    )

    list_display = [
        "id", "label_description", "path", "has_children",
    ]
    list_display_links = [
        "label_description",
    ]
    list_filter = []
    search_fields = [
        "path",
    ]
    readonly_fields = []
    inlines = []
