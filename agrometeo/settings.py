"""Settings."""
# core
STATIONS_ID_NAME = "station_id"
TIME_NAME = "time"

# plotting
PLOT_CMAP = "coolwarm"
PLOT_LEGEND = True
PLOT_ATTRIBUTION = False
PLOT_LEGEND_POSITION = "right"
PLOT_LEGEND_SIZE = "2.5%"
PLOT_LEGEND_PAD = 0.2
PLOT_TITLE = True
PLOT_ADD_BASEMAP = True

# agrometeo specific
DEFAULT_STATIONS_ID_COL = "name"
# https://public.wmo.int/en/programmes/global-climate-observing-system/essential-climate-variables
ECVS = [
    "precipitation",
    "pressure",
    "surface_radiation_longwave",
    "surface_radiation_shortwave",
    "surface_wind_speed",
    "surface_wind_direction",
    "temperature",
    "water_vapour",
]
# agrometeo sensors
# 42                       Leaf moisture III
# 43     Voltage of internal lithium battery
# 1              Temperature 2m above ground
# 4                       Relative humidity
# 6                           Precipitation
# 15              Intensity of precipitation
# 7                            Leaf moisture
# 11                         Solar radiation
# 41                           Solar Energie
# 9                          Avg. wind speed
# 14                         Max. wind speed
# 8                           Wind direction
# 22                       Temperature +10cm
# 12                    Luxmeter after Lufft
# 10                                ETP-Turc
# 24                              ETo-PenMon
# 13                               Dew point
# 18                       Real air pressure
# 2                    Soil temperature +5cm
# 19                  Soil temperature -20cm
# 3                   Soil temperature -10cm
# 5                       Soil moisture -5cm
# 20                   Pressure on sea level
# 17                        Leaf moisture II
# 25                     Soil moisture -30cm
# 26                     Soil moisture -50cm
# 39                                  unused
# 33                 Temperature in leafzone
# 32                         battery voltage
# 21                         min. wind speed
# 23                        Temperatur +20cm
# 27                  Temperatur in Pflanze1
# 28                  Temperatur in Pflanze1
# 29                                    UVAB
# 30                                     UVA
# 31                                     UAB
# 34                Air humidity in leafzone
# 35             Photosyth. active radiation
# 36                  Soil temperature -10cm
# 37                Temperatur 2m unbelüftet
# 38           elative Luftfeuchtigkeit +5cm
# 40                     Precip. Radolan Day
# 100                                   Hour
# 101                                   Year
# 102                            Day of year
# 103                           Degree hours
# 104                 Density of sporulation
# 105                           Leaf surface

ECV_DICT = {
    "precipitation": "Precipitation",
    "pressure": "Real air pressure",
    "surface_radiation_shortwave": "Solar radiation",
    "surface_wind_speed": "Avg. wind speed",
    "surface_wind_direction": "Wind direction",
    "temperature": "Temperature 2m above ground",
    "water_vapour": "Relative humidity",
}
