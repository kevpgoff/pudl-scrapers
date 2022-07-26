"""A command line interface (CLI) to archive data from an RSS feed."""
import argparse
import json
import logging
import re
from pathlib import Path
from zipfile import ZipFile

import feedparser
import requests

import pudl_scrapers.settings
from pudl_scrapers.helpers import new_output_dir

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

FERC_RSS_LINK = "https://ecollection.ferc.gov/api/rssfeed"


def parse_main():
    """Process base commands from the CLI."""
    parser = argparse.ArgumentParser(description="Archive filings from RSS feed")
    parser.add_argument(
        "-r", "--rss-path", default=FERC_RSS_LINK, help="Specify path to RSS feed"
    )
    parser.add_argument(
        "-y", "--year", default=2021, type=int, help="Specify single year for filter"
    )
    parser.add_argument(
        "-f", "--form-number", default=1, type=int, help="Specify form name for filter"
    )
    parser.add_argument(
        "-p", "--period", default=None, help="Specify filing period for filter"
    )

    return parser.parse_args()


def archive_filings(
    feed_path: str,
    form_number: int,
    filter_year: int,
    filter_period: str | None = None,
):
    """Download filings and archive in zipfile.

    Args:
        feed_path: URL or local file path pointing to RSS feed.
        form_number: Form number for filter.
        filter_year: Filing year for filter.
        filter_period: Filing period for filter.
    """
    rss_feed = feedparser.parse(feed_path)

    # Create output directory if it doesn't exist
    output_dir = new_output_dir(
        Path(pudl_scrapers.settings.OUTPUT_DIR) / f"ferc{form_number}"
    )
    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    form_name = f"Form {form_number}"
    archive_path = output_dir / f"ferc{form_number}-{filter_year}.zip"

    logger.info(f"Archiving filings in {archive_path}.")

    # Save JSON file with metadata from RSS feed
    metadata = {}

    with ZipFile(archive_path, "w") as zipfile:
        # Actual link to XBRL filing is only available in inline html
        # This regex pattern will help extract the actual link
        xbrl_link_pat = re.compile(
            r'href="(.+\.(xml|xbrl))">(.+(xml|xbrl))<'
        )  # noqa: W605

        # Loop through entries and filter
        for entry in rss_feed.entries:
            year = int(entry["ferc_year"])

            # Only filter years if a desired year was specified
            if filter_year is not None:
                if year != filter_year:
                    continue

            # Filter form name
            if entry["ferc_formname"] != form_name:
                continue

            # Filter period
            if filter_period is not None:
                if entry["ferc_period"] != filter_period:
                    continue

            # Get link then download filing
            link = xbrl_link_pat.search(entry["summary_detail"]["value"])
            filing = requests.get(link.group(1))

            # Add filing metadata
            filing_name = f"{entry['title']}{entry['ferc_period']}"
            if filing_name in metadata:
                metadata[filing_name].update({entry["id"]: entry})
            else:
                metadata[filing_name] = {entry["id"]: entry}

            # Write to zipfile
            with zipfile.open(f"{entry['id']}.xbrl", "w") as f:
                logger.info(f"Writing {entry['title']} to archive.")
                f.write(filing.text.encode("utf-8"))

        # Save snapshot of RSS feed
        with zipfile.open("rssfeed", "w") as f:
            logger.info("Writing rss feed metadata to archive.")
            f.write(json.dumps(metadata).encode("utf-8"))


def main():
    """CLI for archiving FERC XBRL filings from RSS feed."""
    args = parse_main()

    archive_filings(
        args.rss_path,
        args.form_number,
        filter_year=args.year,
        filter_period=args.period,
    )
