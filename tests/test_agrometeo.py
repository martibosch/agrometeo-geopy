#!/usr/bin/env python
"""Tests for `agrometeo` package."""
# pylint: disable=redefined-outer-name
import numpy as np

import agrometeo as agm


def test_agrometeo():
    # test core functions
    agm_ds = agm.AgrometeoDataset(region="Pully, Switzerland")
    assert agm_ds.CRS is not None
    num_stations = len(agm_ds.station_gdf)
    assert num_stations >= 1
    start_date = "2022-03-22"
    end_date = "2022-03-23"
    ts_df = agm_ds.get_ts_df(start_date=start_date, end_date=end_date)
    assert len(ts_df.columns) == num_stations
    ts_gdf = agm_ds.get_ts_gdf(start_date=start_date, end_date=end_date)
    assert len(ts_gdf) == num_stations
    assert ts_gdf["geometry"].isna().sum() == 0

    # test plotting
    # use `add_basemap=False` to avoid having to mock contextily's requests
    ax = agm.plot_temperature_map(ts_gdf, add_basemap=False)
    assert len(ax.get_title()) > 0
    ax = agm.plot_temperature_map(ts_gdf, title=False, add_basemap=False)
    assert len(ax.get_title()) == 0
    assert len(ax.collections[0].get_array()) == num_stations
    ts_columns = ts_gdf.columns.drop("geometry")
    axes = [
        agm.plot_temperature_map(
            ts_gdf,
            dt=dt,
            add_basemap=False,
        )
        for dt in [ts_columns[0], ts_columns[-1]]
    ]
    assert not np.array_equal(
        axes[0].collections[0].get_array(), axes[1].collections[0].get_array()
    )
