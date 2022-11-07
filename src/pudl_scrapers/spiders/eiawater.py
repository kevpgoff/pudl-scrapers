"""Scrapy spider for the EIA Thermoelectric Cooling Water data."""
import logging
import re
from pathlib import Path

import scrapy
from scrapy.http import Request

from pudl_scrapers import items
from pudl_scrapers.helpers import new_output_dir

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class EiaWaterSpider(scrapy.Spider):
    """Scrapy spider for the EIA Thermoelectric Cooling Water data."""
    name = "eiawater"
    allowed_domains = ["www.eia.gov"]

    def __init__(self, year=None, *args, **kwargs):
        """Initialize the EIA Thermoelectric Cooling Water Spider."""
        super().__init__(*args, **kwargs)

        if year is not None:
            year = int(year)

            if year < 2014:
                raise ValueError("Years before 2014 are not supported")
            if year > 2020:
                raise ValueError("Years after 2020 are not supported")

        self.year = year

    def start_requests(self):
        """Finalize setup and yield the initializing request."""
        # Spider settings are not available during __init__, so finalizing here
        settings_output_dir = Path(self.settings.get("OUTPUT_DIR"))
        output_root = settings_output_dir / "eiawater"
        self.output_dir = new_output_dir(output_root)

        yield Request("https://www.eia.gov/electricity/data/water/")

    def parse(self, response):
        """Parse the eiawater home page.

        Args:
            response (scrapy.http.Response): Must contain the main page

        Yields:
            appropriate follow-up requests to collect XLS files
        """
        if self.year is None:
            yield from self.all_forms(response)

        else:
            yield self.form_for_year(response, self.year)

    # Parsers

    def all_forms(self, response):
        """Produce requests for collectable EIA Thermoelectric Cooling Water forms.

        Args:
            response (scrapy.http.Response): Must contain the main page

        Yields:
            scrapy.http.Requests for EIA Thermoelectric Cooling Water XLS files from 2014 to the most
            recent available
        """
        links = response.xpath(
            "//table[@class='simpletable']//td[3]/a[contains(@href, 'detail') and contains(text(), 'XLS')]"
        )

        for link in links:
            title = link.xpath("@title").extract_first().strip()

            m = re.search(r"\d{4}", title)
            if m:
                year = int(m.group(0))
            else:
                logger.warning(f"No year found in {title}")
                pass

            if year < 2014:
                continue
            if year > 2020:
                continue

            url = response.urljoin(link.xpath("@href").extract_first())

            yield Request(url, meta={"year": year}, callback=self.parse_form)

    def form_for_year(self, response, year):
        """Produce request for a specific EIA Thermoelectric Cooling Water form.

        Args:
            response (scrapy.http.Response): Must contain the main page
            year (int): integer year, 2014 to the most recent available

        Returns:
            Single scrapy.http.Request for EIA Thermoelectric Cooling Water XLS file
        """
        if year < 2014:
            raise ValueError("Years before 2014 are not supported")
        if year > 2020:
            raise ValueError("Years after 2020 are not supported")

        path = (f"//table[@class='simpletable']//td[3]/a[contains(@title, '{year}') and contains(@href, 'detail') and contains(text(), 'XLS')]/@href")

        link = response.xpath(path).extract_first()

        if link is not None:
            url = response.urljoin(link)
            return Request(url, meta={"year": year}, callback=self.parse_form)

    def parse_form(self, response):
        """Produce the EIA Thermoelectric Cooling Water form projects.

        Args:
            response (scrapy.http.Response): Must contain the downloaded XLS file

        Yields:
            items.EiaWater
        """
        path = self.output_dir / f"eiawater-{response.meta['year']}.xlsx"

        yield items.EiaWater(
            data=response.body, year=response.meta["year"], save_path=path
        )
