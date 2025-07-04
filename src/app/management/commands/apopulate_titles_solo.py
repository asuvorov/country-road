"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

import aiohttp
import asyncio

from termcolor import cprint

from django.core.management.base import (
    BaseCommand,
    CommandError)

from ecfr import ECFRClient as client
from ecfr.models import ECFRNode


class Command(BaseCommand):
    """A simple Management Command, which populates the local DB with Titles."""

    help = "Populate the local DB with Titles."

    async def import_data_async(self):
        # ---------------------------------------------------------------------
        # --- Async Method for fetching Article's Content.
        # ---------------------------------------------------------------------
        async def fetch_data(session, tup):
            """Fetch Data."""
            url, obj = tup
            cprint(f"Starting task: {url}", "white")

            while True:
                async with session.get(url) as response:
                    # ---------------------------------------------------------
                    # --- Handle Response Status.
                    #     If the Status Code is different from 200 (e.g. 429, 502, 504) -
                    #     then sleep, and try again.
                    if response.ok:
                        data = await response.content.read()
                        data = str(data.decode()) if isinstance(data, bytes) else str(data)

                        obj.content = data
                        await obj.asave()

                        cprint(f"Completed task: {url}: {len(data)}", "green")
                        # cprint(f"{data}", "green")

                        break

                    cprint(f"Slow down: {response.status}", "white", "on_red")
                    await asyncio.sleep(10)  # Simulating a Delay.

        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Get the List of Titles.
        # ---------------------------------------------------------------------
        titles = client.titles_list()
        cprint(f">>> FOUND {len(titles)} Titles", "cyan")

        # ---------------------------------------------------------------------
        # --- Loop over each Title in Order to fetch Summary and Content, and populate DB.
        # ---------------------------------------------------------------------
        # --- Speed up: Create only one Async Client Session for the entire App.
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60)) as session:
            urls = []
            for k, title in titles.items():
                cprint(f">>> Working on {title["number"]} - {title["name"]}", "cyan")

                date = title["up_to_date_as_of"]
                title = title["number"]

                # -------------------------------------------------------------
                # --- Fetch the Structure of the Title.
                struct = client.title_structure(date, title)
                try:
                    path = f"{struct['type']}-{struct['identifier']}?"
                except Exception as exc:
                    cprint(f"ERROR: {type(exc).__name__}: {str(exc)}", "white", "on_red")
                    continue

                # -------------------------------------------------------------
                # --- Fetch the Content Object from DB.
                obj, created = await ECFRNode.objects.aget_or_create(
                    path=path,
                    identifier=struct["identifier"],
                    label=struct["label"],
                    label_level=struct["label_level"],
                    label_description=struct["label_description"],
                    label_type=struct["type"],
                    # content="",  # content,
                    has_children=False)

                # -------------------------------------------------------------
                # --- Create a Pool of URLs.
                # -------------------------------------------------------------
                # --- Speed up: Skip pulling the Content for the Node, which already has
                #               Content in it.
                if not obj.content:
                    # ---------------------------------------------------------
                    # --- In Fact, this is a List of Tuples (url, obj).
                    urls.append((
                        client.TITLE_CONTENT.format(
                            base_url=client.BASE_URL,
                            date=date,
                            path=path),
                        obj))

            cprint(f"{urls}", "cyan")

            tasks = [fetch_data(session, url) for url in urls]
            results = await asyncio.gather(*tasks)
            # for result in results:
            #     print(result)

    def handle(self, *args, **kwargs):
        """Handler."""
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.import_data_async())
