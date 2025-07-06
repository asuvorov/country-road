"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

import requests

from termcolor import cprint

from django.core.cache import cache


class ECFRClient:
    """eCFR Client."""

    BASE_URL = "https://www.ecfr.gov"

    AGENCIES_SUMMARY = "{base_url}/api/admin/v1/agencies.json"

    TITLES_SUMMARY = "{base_url}/api/versioner/v1/titles.json"
    TITLE_STRUCTURE = "{base_url}/api/versioner/v1/structure/{date}/title-{title}.json"
    TITLE_CORRECTIONS = "{base_url}/api/admin/v1/corrections/title/{title}.json"
    TITLE_CONTENT = "{base_url}/api/renderer/v1/content/enhanced/{date}/{path}"

    def __init__(self, *args, **kwargs):
        """Constructor."""
        super().__init__(*args, **kwargs)

    @classmethod
    def agencies_list(cls, *args, **kwargs):
        """Fetch List of Agencies with their Summaries."""
        agencies = cache.get("agencies")
        if agencies:
            return agencies

        try:
            response = requests.get(cls.AGENCIES_SUMMARY.format(base_url=cls.BASE_URL))
            response.raise_for_status()
        except requests.HTTPError as exc:
            cprint(f"ERROR: {type(exc).__name__}: {str(exc)}", "white", "on_red")
            return {}

        agencies = {a["slug"]: a for a in response.json()["agencies"]}
        cache.set("agencies", agencies, 300)

        return agencies

    @classmethod
    def titles_list(cls, *args, **kwargs):
        """Fetch List of Titles with their Summaries."""
        titles = cache.get("titles")
        if titles:
            return titles

        try:
            response = requests.get(cls.TITLES_SUMMARY.format(base_url=cls.BASE_URL))
            response.raise_for_status()
        except requests.HTTPError as exc:
            cprint(f"ERROR: {type(exc).__name__}: {str(exc)}", "white", "on_red")
            return {}

        titles = {t["number"]: t for t in response.json()["titles"]}
        cache.set("titles", titles, 300)

        return titles

    @classmethod
    def title_structure(cls, date, title, *args, **kwargs):
        """Fetch List of Titles with their Summaries."""
        try:
            response = requests.get(cls.TITLE_STRUCTURE.format(
                base_url=cls.BASE_URL,
                date=date,
                title=title))
            response.raise_for_status()
        except requests.HTTPError as exc:
            cprint(f"ERROR: {type(exc).__name__}: {str(exc)}", "white", "on_red")
            return {}

        return response.json()  # Assuming, the Endpoint returns JSON Object.

    @classmethod
    def title_corrections(cls, title, *args, **kwargs):
        """Fetch List of Title Corrections."""
        try:
            response = requests.get(cls.TITLE_CORRECTIONS.format(
                base_url=cls.BASE_URL,
                title=title))
            response.raise_for_status()
        except requests.HTTPError as exc:
            cprint(f"ERROR: {type(exc).__name__}: {str(exc)}", "white", "on_red")
            return []

        return response.json()["ecfr_corrections"]  # Assuming, the Endpoint returns JSON Object.

    @classmethod
    def title_content(cls, date, path, *args, **kwargs):
        """Fetch List of Titles with their Summaries."""
        try:
            response = requests.get(cls.TITLE_CONTENT.format(
                base_url=cls.BASE_URL,
                date=date,
                path=path))
            response.raise_for_status()
        except requests.HTTPError as exc:
            cprint(f"ERROR: {type(exc).__name__}: {str(exc)}", "white", "on_red")
            return None

        if isinstance(response.content, bytes):
            return str(response.content.decode())

        return str(response.content)
