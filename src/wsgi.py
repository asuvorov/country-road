"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.dev")

application = get_wsgi_application()
