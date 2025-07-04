"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from termcolor import cprint

from app import enum


# =============================================================================
# ===
# === eCFR Node
# ===
# =============================================================================

# -----------------------------------------------------------------------------
# --- eCFR Node Model Choices.
# -----------------------------------------------------------------------------
ECFRNodeType = enum(
    TITLE="title",
    SUBTITLE="subtitle",
    CHAPTER="chapter",
    SUBCHAPTER="subchapter",
    PART="part",
    SUBPART="subpart",
    SUBJECT_GROUP="subject_group",
    SECTION="section",
    APPENDIX="appendix",
)
ecfr_node_type_choices = [
    (ECFRNodeType.TITLE,            _("Title")),
    (ECFRNodeType.SUBTITLE,         _("Subtitle")),
    (ECFRNodeType.CHAPTER,          _("Chapter")),
    (ECFRNodeType.SUBCHAPTER,       _("Subchapter")),
    (ECFRNodeType.PART,             _("Part")),
    (ECFRNodeType.SUBPART,          _("Subpart")),
    (ECFRNodeType.SUBJECT_GROUP,    _("Subject Group")),
    (ECFRNodeType.SECTION,          _("Section")),
    (ECFRNodeType.APPENDIX,         _("Appendix")),
]


# -----------------------------------------------------------------------------
# --- eCFR Node Model Manager.
# -----------------------------------------------------------------------------
class ECFRNodeManager(models.Manager):
    """eCFR Node Manager."""

    def get_queryset(self):
        """Docstring."""
        return super().get_queryset()


# -----------------------------------------------------------------------------
# --- ECFR Node Model.
# -----------------------------------------------------------------------------
class ECFRNode(models.Model):
    """eCFR Node Model."""

    # -------------------------------------------------------------------------
    # --- Basics
    path = models.CharField(
        db_index=True,
        max_length=512,
        verbose_name=_("Path"),
        help_text=_("Path"))

    identifier = models.CharField(
        db_index=True,
        max_length=16,
        verbose_name=_("Identifier"),
        help_text=_("Identifier"))

    label = models.CharField(
        db_index=True,
        max_length=128,
        verbose_name=_("Label"),
        help_text=_("Label"))
    label_level = models.CharField(
        db_index=True,
        max_length=16,
        verbose_name=_("Label Level"),
        help_text=_("Label Level"))
    label_description = models.CharField(
        db_index=True,
        max_length=128,
        verbose_name=_("Label Description"),
        help_text=_("Label Description"))
    label_type = models.CharField(
        max_length=16,
        choices=ecfr_node_type_choices, default=ECFRNodeType.TITLE,
        verbose_name=_("Label Type"),
        help_text=_("Label Type"))

    content = models.TextField(
        null=True, blank=True,
        verbose_name=_("Content"),
        help_text=_("Content"))

    # -------------------------------------------------------------------------
    # --- Flags
    has_children = models.BooleanField(
        default=False,
        verbose_name=_("Has Children Nodes?"),
        help_text=_("Has Children Nodes?"))

    objects = ECFRNodeManager()

    class Meta:
        app_label = "ecfr"
        verbose_name = _("eCFR Node")
        verbose_name_plural = _("eCFR Nodes")
        ordering = ["id", "path"]

    def __repr__(self):
        """Docstring."""
        return f"<{self.__class__.__name__} ({self.id}: '{self.label_description}')>"

    def __str__(self):
        """Docstring."""
        return self.__repr__()
