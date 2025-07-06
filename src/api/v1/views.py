"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

import hashlib
import re

from bs4 import BeautifulSoup
from termcolor import cprint

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from ecfr import ECFRClient as client
from ecfr.models import ECFRNode


class APIAgencyStatsViewSet(APIView):
    """Agency Stats View Set."""

    permission_classes = (AllowAny, )
    renderer_classes = (JSONRenderer, )

    def get(self, request):
        """GET: Agency Stats."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        data = []

        # ---------------------------------------------------------------------
        # --- Retrieve Data from the Request.
        # ---------------------------------------------------------------------
        slug = request.query_params.get("slug", "")
        cprint(f"{slug=}", "cyan")

        # ---------------------------------------------------------------------
        # --- Handle Errors.
        # ---------------------------------------------------------------------
        if not slug:
            return Response({
                "message":      "No Slug provided.",
            }, status=status.HTTP_400_BAD_REQUEST)

        agencies = client.agencies_list()
        if slug not in agencies:
            return Response({
                "message":      "Invalid Request.",
            }, status=status.HTTP_400_BAD_REQUEST)

        titles = client.titles_list()
        cprint(f">>> FOUND {len(titles)} Titles", "cyan")

        # ---------------------------------------------------------------------
        # --- Prepare Response.
        # ---------------------------------------------------------------------
        content = ""
        agency = agencies[slug]
        cfr_references = len(agency["cfr_references"])
        cfr_corrections = 0

        for cfr_reference in agency["cfr_references"]:
            title = cfr_reference["title"]
            title_path = f"title-{title}?"
            title_date = titles[title]["up_to_date_as_of"]
            entry_path = title_path

            del cfr_reference["title"]

            for k, v in cfr_reference.items():
                entry_path += f"{k}={v}&"

            # -----------------------------------------------------------------
            # --- Calculate Corrections.
            agency_ref_corrections = []
            title_corrections = []
            for tcs in client.title_corrections(title=title):
                for cfr_ref in tcs["cfr_references"]:
                    title_corrections.append(cfr_ref)

            cprint(f"FOUND {len(title_corrections)} Title Corrections", "yellow")

            # -----------------------------------------------------------------
            # --- Sort out the Corrections, only related to the given Agency.
            for k, v in cfr_reference.items():
                cprint(f"REMAINING {len(title_corrections)} Title Corrections", "yellow")
                for tc in title_corrections:
                    if (
                            k in tc["hierarchy"] and
                            tc["hierarchy"][k] == str(v)):
                        agency_ref_corrections.append(tc)
                cprint(f"FOUND {len(agency_ref_corrections)} AGENCY Corrections", "yellow")

                title_corrections = agency_ref_corrections
                agency_ref_corrections = []

            cfr_corrections += len(title_corrections)

            # -----------------------------------------------------------------
            # --- Get or create DB Fallback.
            try:
                entry = ECFRNode.objects.get(path=entry_path)
                cprint("Entry: DB HIT", "green")
            except ECFRNode.DoesNotExist:
                cprint("Entry: DB MISS", "red")
                title_content = client.title_content(
                    date=title_date,
                    path=entry_path)
                entry, created = ECFRNode.objects.get_or_create(
                    path=entry_path,
                    identifier=titles[title]["number"],
                    label=titles[title]["name"],
                    label_level=titles[title]["number"],
                    label_description=titles[title]["name"],
                    label_type="title",
                    content=title_content,
                    has_children=False)

            entry_content = entry.content

            # -----------------------------------------------------------------
            # --- Purge the <script> Tags.
            soup = BeautifulSoup(entry_content, "lxml")
            script_tags = soup.find_all("script")
            for script in script_tags:
                script.decompose()
            entry_content = str(soup)

            # -----------------------------------------------------------------
            # --- Clean up the Tags.
            clean = re.compile('<.*?>')
            entry_content = re.sub(clean, "", entry_content)

            content += entry_content

        # ---------------------------------------------------------------------
        # --- Count the Words.
        # ---------------------------------------------------------------------
        words = re.findall(r'\b\w+\b', content)
        word_count = len(words)
        cprint(f"{word_count=}", "white", "on_red")

        data.append({
            "agency":           agency["name"],
            "cfr_references":   cfr_references,
            "cfr_corrections":  cfr_corrections,
            "word_count":       word_count,
            "checksum":         hashlib.md5(content.encode()).hexdigest(),
        })
        cprint(f"{data=}", "cyan")

        return Response(data, status=status.HTTP_200_OK)


api_agency_stats = APIAgencyStatsViewSet.as_view()


class APITitleStatsViewSet(APIView):
    """Title Stats View Set."""

    permission_classes = (AllowAny, )
    renderer_classes = (JSONRenderer, )

    def get(self, request):
        """GET: Title Stats."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        data = []

        # ---------------------------------------------------------------------
        # --- Retrieve Data from the Request.
        # ---------------------------------------------------------------------
        slug = int(request.query_params.get("slug", ""))
        cprint(f"{slug=}", "cyan")

        # ---------------------------------------------------------------------
        # --- Handle Errors.
        # ---------------------------------------------------------------------
        if not slug:
            return Response({
                "message":      "No Slug provided.",
            }, status=status.HTTP_400_BAD_REQUEST)

        titles = client.titles_list()
        if slug not in titles:
            return Response({
                "message":      "Invalid Request.",
            }, status=status.HTTP_400_BAD_REQUEST)

        agencies = client.agencies_list()

        # ---------------------------------------------------------------------
        # --- Prepare Response.
        # ---------------------------------------------------------------------
        title = titles[slug]
        agency_references = []
        cfr_corrections = 0

        # ---------------------------------------------------------------------
        # --- Get all the Agencies References in this Title.
        # ---------------------------------------------------------------------
        for k, v in agencies.items():
            for cfr_reference in v["cfr_references"]:
                if cfr_reference["title"] == slug:
                    agency_references.append(v["name"])

        # ---------------------------------------------------------------------
        # --- Get all the CFR Correction in this Title.
        # ---------------------------------------------------------------------
        cfr_corrections = len(client.title_corrections(title=slug))

        data.append({
            "title":                f"{title['number']} - {title['name']}",
            "agency_references":    "<br>".join(list(set(agency_references))),
            "cfr_corrections":      cfr_corrections,
        })
        cprint(f"{data=}", "cyan")

        return Response(data, status=status.HTTP_200_OK)


api_title_stats = APITitleStatsViewSet.as_view()
