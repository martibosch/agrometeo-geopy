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

from . import base, settings

__all__ = ["AgrometeoDataset"]

# API endpoints
BASE_URL = "https://www.agrometeo.ch/backend/api"
# the agrometeo API uses integer ids to identify stations, which can be retrieved from
# the "id" column of the stations dataframe
STATIONS_API_ID_COL = "id"
STATIONS_API_ENDPOINT = path.join(BASE_URL, "stations")
VARIABLES_NAME_COL = "name.en"
VARIABLES_CODE_COL = "id"
VARIABLES_API_ENDPOINT = path.join(BASE_URL, "sensors")
# note that there is a `stations/near` endpoint as in:
# stations/near?latitude=46.433&longitude=6.9114
METEO_DATA_API_ENDPOINT = path.join(BASE_URL, "meteo/data")

# useful constants
LONLAT_CRS = "epsg:4326"
LV03_CRS = "epsg:21781"
GEOM_COL_DICT = {LONLAT_CRS: ["long_dec", "lat_dec"], LV03_CRS: ["lon_ch", "lat_ch"]}
API_DT_FMT = "%Y-%m-%d"
SJOIN_PREDICATE = "within"
SCALE = "none"
MEASUREMENT = "avg"


class AgrometeoDataset(base.MeteoStationDataset):
    """Agrometeo dataset."""

    def __init__(
        self,
        *,
        region=None,
        stations_id_name=None,
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
        # ACHTUNG: need to define the CRS before calling the parent's init
        if crs is None:
            crs = LONLAT_CRS
        self.crs = crs

        super().__init__(
            region=region,
            stations_id_name=stations_id_name,
            time_name=time_name,
            geocode_to_gdf_kws=geocode_to_gdf_kws,
        )

        if sjoin_kws is None:
            sjoin_kws = {}
        self.sjoin_kws = sjoin_kws

    @property
    def CRS(self):  # pylint: disable=invalid-name
        """CRS of the data source."""
        return self.crs

    @property
    def stations_gdf(self):
        """Station geo-data frame."""
        try:
            return self._stations_gdf
        except AttributeError:
            geom_cols = GEOM_COL_DICT[self.crs]
            response = requests.get(STATIONS_API_ENDPOINT)
            stations_df = pd.json_normalize(response.json()["data"])
            # it is fine to filter out this ShapelyDeprecationWarning, see
            # https://shapely.readthedocs.io/en/latest/migration.html
            # #creating-numpy-arrays-of-geometry-objects
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)
                stations_gdf = gpd.GeoDataFrame(
                    stations_df.drop(geom_cols, axis=1),
                    geometry=stations_df[geom_cols]
                    .astype(np.float64)
                    .apply(lambda xy_ser: Point(xy_ser[0], xy_ser[1]), axis=1),
                    crs=self.crs,
                )

            _sjoin_kws = self.sjoin_kws.copy()
            predicate = _sjoin_kws.pop("predicate", SJOIN_PREDICATE)
            stations_gdf = stations_gdf.sjoin(
                self.region.to_crs(stations_gdf.crs), predicate=predicate, **_sjoin_kws
            )
            # stations_gdf.index.name = self.stations_id_name

            self._stations_gdf = stations_gdf

            return self._stations_gdf

    @property
    def variables_df(self):
        """Variables data frame."""
        try:
            return self._variables_df
        except AttributeError:
            response = requests.get(VARIABLES_API_ENDPOINT)
            variables_df = pd.json_normalize(response.json()["data"])

            # ACHTUNG: need to strip strings, at least in variables name column. Note
            # that *it seems* that the integer type of variable code column is inferred
            # correctly
            variables_df[VARIABLES_NAME_COL] = variables_df[
                VARIABLES_NAME_COL
            ].str.strip()

            self._variables_df = variables_df

            return self._variables_df

    def _get_region_data(self, variable_code, start_date, end_date, scale, measurement):
        # use a variable for the station ids just to keep the line below shorter
        _stations_ids = self.stations_gdf[STATIONS_API_ID_COL].astype(str)
        request_url = f"{METEO_DATA_API_ENDPOINT}?" + "&".join(
            [
                f"from={start_date}",
                f"to={end_date}",
                f"scale={scale}",
                f"sensors={variable_code}%3A{measurement}",
                f"stations={'%2C'.join(_stations_ids)}",
            ]
        )

        return requests.get(request_url)

    def get_ts_df(
        self,
        variable,
        start_date,
        end_date,
        *,
        scale=None,
        measurement=None,
        stations_id_col=None,
    ):
        """
        Get time series data frame.

        Parameters
        ----------
        variable : str or int
            Target variable, which can be either an agrometeo variable code (integer or
            string), an essential climate variable (ECV) following the
            meteostations-geopy nomenclature (string), or an agrometeo variable name
            (string).
        start_date, end_date : str or datetime
            String in the "YYYY-MM-DD" format or datetime instance, respectively
            representing the start and end of the  requested data period.
        scale : None or {"hour", "day", "month", "year"}, default None
            Temporal scale of the measurements. The default value of None returns the
            finest scale, i.e., 10 minutes.
        measurement : {"min", "avg", "max"}, default "avg"
            Whether the measurement values correspond to the minimum, average or maximum
            value for the required temporal scale. Ignored if `scale` is None.
        stations_id_col : str, optional
            Column of `stations_gdf` that will be used in the returned data frame to
            identify the stations. If None, the value from
            `settings.DEFAULT_STATIONS_ID_COL` will be used.

        Returns
        -------
        ts_df : pd.DataFrame
            Data frame with a time series of meaurements (rows) at each station
            (columns).
        """
        # process the variable arg
        # variable is a string that can be either:
        # a) an agrometeo variable code
        # b) an essential climate variable (ECV) following the meteostations-geopy
        # nomenclature
        # c) an agrometeo variable name
        if isinstance(variable, int) or variable.isdigit():
            # case a: if variable is an integer, assert that it is a valid variable code
            variable_code = int(variable)
            if variable_code not in self.variables_df[VARIABLES_CODE_COL].values:
                raise ValueError(
                    f"variable {variable} is not a valid agrometeo variable code"
                )
        else:
            # case b or c: if variable is an ECV, it will be a key in the ECV_DICT so
            # the agrometeo variable code can be retrieved directly, otherwise we
            # assume that variable is an agrometeo variable name
            agm_variable_name = settings.ECV_DICT.get(variable, variable)
            variable_code = self.variables_df.loc[
                self.variables_df[VARIABLES_NAME_COL] == agm_variable_name,
                VARIABLES_CODE_COL,
            ].item()
        # process date args
        if isinstance(start_date, datetime.datetime):
            start_date = start_date.strftime(API_DT_FMT)
        if isinstance(end_date, datetime.datetime):
            end_date = end_date.strftime(API_DT_FMT)
        # process scale and measurement args
        if scale is None:
            # the API needs it to be lowercase
            scale = SCALE
        if measurement is None:
            measurement = MEASUREMENT
        # process the stations_id_col arg
        if stations_id_col is None:
            stations_id_col = settings.DEFAULT_STATIONS_ID_COL

        # query the API
        response = self._get_region_data(
            variable_code, start_date, end_date, scale, measurement
        )

        # parse the response as a data frame
        ts_df = pd.json_normalize(response.json()["data"]).set_index("date")
        ts_df.index = pd.to_datetime(ts_df.index)
        ts_df.index.name = self.time_name
        # ts_df.columns = self.stations_gdf[STATIONS_ID_COL]
        # ACHTUNG: note that agrometeo returns the data indexed by keys of the form
        # "{station_id}_{variable_code}_{measurement}", so to properly set the columns
        # as the desired station identifier (e.g., "id" or "name") we need to first get
        # the ids and then get (loc) the station data from the stations_gdf.
        ts_df.columns = self.stations_gdf.set_index(STATIONS_API_ID_COL).loc[
            ts_df.columns.str.replace(f"_{variable_code}_{measurement}", "").astype(
                self.stations_gdf[STATIONS_API_ID_COL].dtype
            )
        ][stations_id_col]
        ts_df = ts_df.apply(pd.to_numeric, axis=1)

        return ts_df.sort_index()

    def get_ts_gdf(
        self,
        variable,
        start_date,
        end_date,
        *,
        scale=None,
        measurement=None,
        stations_id_col=None,
    ):
        """
        Get time series geo-data frame.

        Parameters
        ----------
        variable : str or int
            Target variable, which can be either an agrometeo variable code (integer or
            string), an essential climate variable (ECV) following the
            meteostations-geopy nomenclature (string), or an agrometeo variable name
            (string).
        start_date, end_date : str or datetime
            String in the "YYYY-MM-DD" format or datetime instance, respectively
            representing the start and end of the  requested data period.
        scale : None or {"hour", "day", "month", "year"}, default None
            Temporal scale of the measurements. The default value of None returns the
            finest scale, i.e., 10 minutes.
        measurement : {"min", "avg", "max"}, default "avg"
            Whether the measurement values correspond to the minimum, average or maximum
            value for the required temporal scale. Ignored if `scale` is None.
        stations_id_col : str, optional
            Column of `stations_gdf` that will be used in the returned data frame to
            identify the stations. If None, the value from
            `settings.DEFAULT_STATIONS_ID_COL` is used.

        Returns
        -------
        ts_gdf : gpd.GeoDataFrame
            Geo-data frame with a time series of meaurements (columns) at each station
            (rows), with an additional geometry column with the stations' locations.
        """
        ts_gdf = gpd.GeoDataFrame(
            self.get_ts_df(
                variable,
                start_date,
                end_date,
                scale=scale,
                measurement=measurement,
                stations_id_col=stations_id_col,
            ).T
        )
        # get the geometry from stations_gdf
        ts_gdf["geometry"] = self.stations_gdf.set_index(ts_gdf.index.name).loc[
            ts_gdf.index
        ]["geometry"]
        # sort the timestamp columns
        ts_columns = ts_gdf.columns.drop("geometry")
        ts_gdf = ts_gdf[sorted(ts_columns) + ["geometry"]]

        return ts_gdf
