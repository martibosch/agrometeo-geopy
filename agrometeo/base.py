"""Base abstract classes for meteo station datasets."""
import abc
import logging

import geopandas as gpd
import pandas as pd
from fiona.errors import DriverError

try:
    import osmnx as ox
except ImportError:
    ox = None

from . import settings

__all__ = ["MeteoStationDataset"]


def _process_region_arg(region=None, geocode_to_gdf_kws=None):
    if region is not None:
        if isinstance(region, gpd.GeoSeries):
            # if we have a GeoSeries, convert it to a GeoDataFrame so that we can use
            # the same code
            region = gpd.GeoDataFrame(geometry=region)
        elif not isinstance(region, gpd.GeoDataFrame):
            # at this point, we assume that this is either file-like or a Nominatim
            # query
            try:
                region = gpd.read_file(region)
            except DriverError:
                if ox is None:
                    logging.warning(
                        """
Using a Nominatim query as `region` argument requires the osmnx package. You can install
it using conda or pip. See https://github.com/geopandas/geopandas.
"""
                    )
                    return

                if geocode_to_gdf_kws is None:
                    geocode_to_gdf_kws = {}
                region = ox.geocode_to_gdf(region, **geocode_to_gdf_kws).iloc[:1]

    return region


def _long_ts_df(ts_df, station_id_name, time_name, value_name):
    """Transform time series data frame from wide (default) to long format."""
    return pd.melt(
        ts_df.reset_index(),
        id_vars=time_name,
        var_name=station_id_name,
        value_name=value_name,
    )


class MeteoStationDataset(metaclass=abc.ABCMeta):
    """Meteo station dataset."""

    def __init__(
        self,
        *,
        region=None,
        station_id_name=None,
        time_name=None,
        geocode_to_gdf_kws=None,
    ):
        """
        Initialize an meteo station dataset.

        Parameters
        ----------
        region : str, list-like, geopandas.GeoSeries, geopandas.GeoDataFrame, geometric
                 object, file-like object or pathlib.Path object, optional
            This can either be:

            * A string with a Nominatim query to geocode
            * A list-like with the west, south, east and north bounds
            * A geopandas geo-series or geo-data frame
            * A geometric object, e.g., shapely geometry
            * A filename or URL, a file-like object opened in binary ('rb') mode, or a
              Path object that will be passed to `geopandas.read_file`.
        """
        self.region = _process_region_arg(
            region=region, geocode_to_gdf_kws=geocode_to_gdf_kws
        )
        if station_id_name is None:
            station_id_name = settings.STATION_ID_NAME
        self.station_id_name = station_id_name
        if time_name is None:
            time_name = settings.TIME_NAME
        self.time_name = time_name

    @abc.abstractproperty
    def station_gdf(self):
        """Station geo-data frame."""
        pass

    @abc.abstractmethod
    def get_ts_df(self, *args, **kwargs):
        """
        Get time series data frame.

        Returns
        -------
        ts_df : pd.DataFrame
            Data frame with a time series of meaurements (rows) at each station
            (columns).
        """
        pass

    @abc.abstractmethod
    def get_ts_gdf(self, *args, **kwargs):
        """
        Get time series geo-data frame.

        Returns
        -------
        ts_gdf : gpd.GeoDataFrame
            Geo-data frame with a time series of meaurements (columns) at each station
            (rows), with an additional geometry column with the stations' locations.
        """
        pass
