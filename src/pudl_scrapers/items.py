"""Data model definitions for the PUDL raw data itmes being scraped.

See documentation in: https://docs.scrapy.org/en/latest/topics/items.html
"""

import scrapy


class DataFile(scrapy.Item):
    """A generic binary data file Item."""

    data = scrapy.Field()  # file binary
    save_path = scrapy.Field(serializer=str)


class Eia860(DataFile):
    """The Eia860 forms in a zip file."""

    year = scrapy.Field(serializer=int)

    def __repr__(self):
        """String representation of an EIA-860 data file."""
        return f"Eia860(year={self['year']}, save_path='{self['save_path']}')"


class Eia860M(DataFile):
    """The EIA 860 M forms in a xlsx file."""

    year = scrapy.Field(serializer=int)
    month = scrapy.Field(serializer=str)

    def __repr__(self):
        """String representation of an EIA-860M data file."""
        return (
            f"Eia860M(year={self['year']}, month={self['month']}, "
            f"save_path={self['save_path']})"
        )


class Eia861(DataFile):
    """The Eia861 forms in a zip file."""

    year = scrapy.Field(serializer=int)

    def __repr__(self):
        """String representation of an EIA-861 data file."""
        return f"Eia861(year={self['year']}, save_path='{self['save_path']}')"


class Eia923(DataFile):
    """The Eia923 forms in a zip file."""

    year = scrapy.Field(serializer=int)

    def __repr__(self):
        """String representation of an EIA-923 data file."""
        return f"Eia923(year={self['year']}, save_path='{self['save_path']}')"


class EiaWater(DataFile):
    """The EIA Thermoelectric Cooling Water forms in an xlsx file."""

    year = scrapy.Field(serializer=int)

    def __repr__(self):
        """String representation of an EIA Thermoelectric Cooling Water data file."""
        return f"EiaWater(year={self['year']}, save_path='{self['save_path']}')"


class Ferc1(DataFile):
    """The Ferc1 forms in a zip file."""

    year = scrapy.Field(serializer=int)

    def __repr__(self):
        """String representation of a FERC-1 data file."""
        return f"Ferc1(year={self['year']}, save_path='{self['save_path']}')"


class Ferc2(DataFile):
    """The Ferc2 forms in a zip file."""

    year = scrapy.Field(serializer=int)
    part = scrapy.Field(serializer=int)

    def __repr__(self):
        """String representation of a FERC-2 data file."""
        return f"Ferc2(year={self['year']}, part={self['part']}, save_path='{self['save_path']}')"


class Ferc6(DataFile):
    """The FERC Form 6 in a zip file."""

    year = scrapy.Field(serializer=int)

    def __repr__(self):
        """String representation of a FERC-6 data file."""
        return f"Ferc6(year={self['year']}, save_path='{self['save_path']}')"


class Ferc60(DataFile):
    """The FERC Form 60 in a zip file."""

    year = scrapy.Field(serializer=int)

    def __repr__(self):
        """String representation of a FERC-60 data file."""
        return f"Ferc60(year={self['year']}, save_path='{self['save_path']}')"


class Ferc714(DataFile):
    """The Ferc714 data zip file."""

    def __repr__(self):
        """String representation of a FERC-714 data file."""
        return f"Ferc714('{self['save_path']}')"


class EpaCamdEia(DataFile):
    """The EPA CAMD to EIA Crosswalk zip file."""

    def __repr__(self):
        """String representation of the EPA CAMD to EIA Crosswalk data file."""
        return f"EpaCamdEia('{self['save_path']}')"


class Cems(DataFile):
    """A CEMS zip file."""

    def __repr__(self):
        """String representation of an EPA CEMS data file."""
        return f"Cems(save_path='{self['save_path']}')"


class Census(DataFile):
    """Census zip file."""

    def __repr__(self):
        """String representation of the Census DP1 data file."""
        return f"Census(save_path='{self['save_path']}')"
