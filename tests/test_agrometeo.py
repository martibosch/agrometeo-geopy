#!/usr/bin/env python
"""Tests for `agrometeo` package."""
# pylint: disable=redefined-outer-name
from datetime import datetime, timedelta

import agrometeo as agm


def test_core():
    agm_ds = agm.AgrometeoDataset(region="Pully, Switzerland")
    num_stations = len(agm_ds.station_gdf)
    assert num_stations >= 1
    today = datetime.today()
    start_date = today - timedelta(days=2)
    end_date = today - timedelta(days=1)
    ts_df = agm_ds.get_ts_df(start_date=start_date, end_date=end_date)
    assert len(ts_df.columns) == num_stations
    ts_gdf = agm_ds.get_ts_gdf(start_date=start_date, end_date=end_date)
    assert len(ts_gdf) == num_stations
