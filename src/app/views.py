"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

from django.shortcuts import render

from ecfr import ECFRClient as client
from ecfr.models import ECFRNode


# =============================================================================
# ===
# === INDEX
# ===
# =============================================================================
def index(request):
    """Docstring."""
    # -------------------------------------------------------------------------
    # --- Initials.
    # -------------------------------------------------------------------------
    agencies = client.agencies_list()
    titles = client.titles_list()

    return render(
        request, "app/index.html", {
            "agencies":     agencies,
            "titles":       titles,
        })
