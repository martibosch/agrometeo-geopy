"""Agrometeo."""
import datetime
import warnings
from os import path

import geopandas as gpd
import numpy as np
import pandas as pd
import requests
from shapely.errors import ShapelyDeprecationWarning
from shapely.geometry import Point

from . import base

all = ["AgrometeoDataset"]

# API endpoints
BASE_URL = "https://www.agrometeo.ch/backend/api"
STATIONS_API_ENDPOINT = path.join(BASE_URL, "stations")
# note that there is a `stations/near` endpoint as in:
# stations/near?latitude=46.433&longitude=6.9114
METEO_DATA_API_ENDPOINT = path.join(BASE_URL, "meteo/data")

# useful constants
LONLAT_CRS = "epsg:4326"
LV03_CRS = "epsg:21781"
GEOM_COL_DICT = {LONLAT_CRS: ["long_dec", "lat_dec"], LV03_CRS: ["lon_ch", "lat_ch"]}
API_DT_FMT = "%Y-%m-%d"
STATION_ID_COL = "name"
SJOIN_PREDICATE = "within"
MEASUREMENT = "avg"


class AgrometeoDataset(base.MeteoStationDataset):
    """Agrometeo dataset."""

    def __init__(
        self,
        *,
        region=None,
        station_id_name=None,
        time_name=None,
        crs=None,
        geocode_to_gdf_kws=None,
        sjoin_kws=None,
    ):
        """
        Initialize an Agrometeo dataset.

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
        super().__init__(
            region=region,
            station_id_name=station_id_name,
            time_name=time_name,
            geocode_to_gdf_kws=geocode_to_gdf_kws,
        )

        if crs is None:
            crs = LONLAT_CRS
        self.crs = crs

        if sjoin_kws is None:
            sjoin_kws = {}
        self.sjoin_kws = sjoin_kws

    @property
    def station_gdf(self):
        """Station geo-data frame."""
        try:
            return self._station_gdf
        except AttributeError:
            geom_cols = GEOM_COL_DICT[self.crs]
            response = requests.get(STATIONS_API_ENDPOINT)
            station_df = pd.json_normalize(response.json()["data"]).set_index("id")
            # it is fine to filter out this ShapelyDeprecationWarning, see
            # https://shapely.readthedocs.io/en/latest/migration.html
            # #creating-numpy-arrays-of-geometry-objects
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)
                station_gdf = gpd.GeoDataFrame(
                    station_df.drop(geom_cols, axis=1),
                    geometry=station_df[geom_cols]
                    .astype(np.float64)
                    .apply(lambda xy_ser: Point(xy_ser[0], xy_ser[1]), axis=1),
                    crs=self.crs,
                )

            _sjoin_kws = self.sjoin_kws.copy()
            predicate = _sjoin_kws.pop("predicate", SJOIN_PREDICATE)
            station_gdf = station_gdf.sjoin(
                self.region.to_crs(station_gdf.crs), predicate=predicate, **_sjoin_kws
            )
            # station_gdf.index.name = self.station_id_name

            self._station_gdf = station_gdf

            return self._station_gdf

    def _get_region_data(self, start_date, end_date, *, scale=None, measurement=None):

        if isinstance(start_date, datetime.datetime):
            start_date = start_date.strftime(API_DT_FMT)
        if isinstance(end_date, datetime.datetime):
            end_date = end_date.strftime(API_DT_FMT)
        if scale is None:
            # the API needs it to be lowercase
            scale = "none"
        if measurement is None:
            measurement = MEASUREMENT

        request_url = f"{METEO_DATA_API_ENDPOINT}?" + "&".join(
            [
                f"from={start_date}",
                f"to={end_date}",
                f"scale={scale}",
                f"sensors=1%3A{measurement}",
                f"stations={'%2C'.join(self.station_gdf.index.astype(str))}",
            ]
        )

        return requests.get(request_url)

    def get_ts_df(self, start_date, end_date, *, scale=None, measurement=None):
        """
        Get time series data frame.

        Parameters
        ----------
        start_date, end_date : str or datetime
            String in the "YYYY-MM-DD" format or datetime instance, respectively
            representing the start and end of the  requested data period.
        scale : None or {"hour", "day", "month", "year"}, default None
            Temporal scale of the measurements. The default value of None returns the
            finest scale, i.e., 10 minutes.
        measurement : {"min", "avg", "max"}, default "avg"
            Whether the measurement values correspond to the minimum, average or maximum
            value for the required temporal scale. Ignored if `scale` is None.

        Returns
        -------
        ts_df : pd.DataFrame
            Data frame with a time series of meaurements (rows) at each station
            (columns).
        """
        response = self._get_region_data(
            start_date, end_date, scale=scale, measurement=measurement
        )
        ts_df = pd.json_normalize(response.json()["data"]).set_index("date")
        ts_df.index = pd.to_datetime(ts_df.index)
        ts_df.index.name = self.time_name
        ts_df.columns = self.station_gdf[STATION_ID_COL]
        ts_df = ts_df.apply(pd.to_numeric, axis=1)

        return ts_df

    def get_ts_gdf(self, region, start_date, end_date, *, scale=None, measurement=None):
        """
        Get time series geo-data frame.

        Parameters
        ----------
        start_date, end_date : str or datetime
            String in the "YYYY-MM-DD" format or datetime instance, respectively
            representing the start and end of the  requested data period.
        scale : None or {"hour", "day", "month", "year"}, default None
            Temporal scale of the measurements. The default value of None returns the
            finest scale, i.e., 10 minutes.
        measurement : {"min", "avg", "max"}, default "avg"
            Whether the measurement values correspond to the minimum, average or maximum
            value for the required temporal scale. Ignored if `scale` is None.

        Returns
        -------
        ts_gdf : gpd.GeoDataFrame
            Geo-data frame with a time series of meaurements (columns) at each station
            (rows), with an additional geometry column with the stations' locations.
        """
        ts_gdf = gpd.GeoDataFrame(
            self.get_ts_df(),
            geometry=self.station_gdf["geometry"],
        )
        ts_columns = ts_gdf.columns.drop("geometry")
        ts_gdf = ts_gdf[sorted(ts_columns) + ["geometry"]]
        ts_gdf.columns = pd.to_datetime() + ["geometry"]

        return ts_gdf
