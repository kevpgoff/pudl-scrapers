"""Test the EIA Thermoelectric Cooling Water Spider."""
from pudl_scrapers.spiders.eiawater import EiaWaterSpider
from tests import factories


class TestEiaWater:
    """Validate EIA Thermoelectric Cooling Water Spider."""

    def test_spider_ids_files(self):
        """Eia Water spider parses zip file links."""
        spider = EiaWaterSpider()
        resp = factories.TestResponseFactory(eiawater=True)
        result = list(spider.all_forms(resp))
        assert (
            result[0].url == "https://www.eia.gov/electricity/data/water"
            "/xls/cooling_detail_2020.xlsx"
        )
        assert result[0].meta["year"] == 2020
        assert (
            result[-1].url == "https://www.eia.gov/electricity/data/water"
            "/archive/xls/cooling_detail_2014.xlsx"
        )
        assert result[-1].meta["year"] == 2014

    def test_spider_gets_specific_year(self):
        """Eia Water spider can pick forms for a specific year."""
        spider = EiaWaterSpider()
        resp = factories.TestResponseFactory(eiawater=True)

        result = spider.form_for_year(resp, 2014)

        assert result is not None
        assert (
            result.url == "https://www.eia.gov/electricity/data/water"
            "/archive/xls/cooling_detail_2014.xlsx"
        )
        assert result.meta["year"] == 2014

        for year in range(2014, 2020):
            result = spider.form_for_year(resp, year)
            assert result is not None

        for year in [2013, 2021]:
            try:
                result = spider.form_for_year(resp, year)
            except ValueError as e:
                assert 'not supported' in str(e)
