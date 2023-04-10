# History

## 0.2.0 (2023-04-10)

### Feat

- bump version to 0.2.0
- support multiple vars; station_id_col as setting
- sort_index in ts_df

### Fix

- avoid AttributeError when no contextily and add_basemap is True

### Refactor

- rename station -> stations in constants for consistency

## 0.1.3 (2023-04-03)

- fix: set columns based on str replace

## 0.1.2 (2022-03-21)

- fix: missing default plot settings; added plotting tests
- fix: geometry column in `ts_gdf`

## 0.1.1 (2022-03-21)

- fix: drop region arg in get_ts_gdf, forward args to get_ts_df
- fixed "all" imports in core and plotting

## 0.1.0 (2022-03-10)

- First release on PyPI.
