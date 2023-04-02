[![PyPI version fury.io](https://badge.fury.io/py/agrometeo-geopy.svg)](https://pypi.python.org/pypi/agrometeo-geopy/)
[![Documentation Status](https://readthedocs.org/projects/agrometeo-geopy/badge/?version=latest)](https://agrometeo-geopy.readthedocs.io/en/latest/?badge=latest)
[![CI/CD](https://github.com/martibosch/agrometeo-geopy/actions/workflows/dev.yml/badge.svg)](https://github.com/martibosch/agrometeo-geopy/blob/main/.github/workflows/dev.yml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/martibosch/agrometeo-geopy/main.svg)](https://results.pre-commit.ci/latest/github/martibosch/agrometeo-geopy/main)
[![codecov](https://codecov.io/gh/martibosch/agrometeo-geopy/branch/main/graph/badge.svg?token=hKoSSRn58a)](https://codecov.io/gh/martibosch/agrometeo-geopy)
[![GitHub license](https://img.shields.io/github/license/martibosch/agrometeo-geopy.svg)](https://github.com/martibosch/agrometeo-geopy/blob/main/LICENSE)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/martibosch/agrometeo-geopy/HEAD?labpath=docs%2Fusage.ipynb)

# agrometeo-geopy

Pythonic interface to access [agrometeo.ch](https://agrometeo.ch) data.

## Installation

The agrometeo-geopy library requires [geopandas](https://geopandas.org/), which can be installed using conda/mamba as in:

```shell
conda install -c conda-forge geopandas
```

Then, agrometeo-geopy can be installed using pip:

```shell
pip install agrometeo-geopy
```

## Overview

```python
import agrometeo as agm

start_date = "2021-08-13"
end_date = "2021-08-16"

agm_ds = agm.AgrometeoDataset(region="Canton de Genève")
ts_df = agm_ds.get_ts_df(start_date=start_date, end_date=end_date)
ts_df
```

<div>
    <div class="wy-table-responsive"><table border="1" class="dataframe docutils">
            <thead>
                <tr style="text-align: right;">
                    <th>name</th>
                    <th>DARDAGNY</th>
                    <th>LA-PLAINE</th>
                    <th>SATIGNY</th>
                    <th>PEISSY</th>
                    <th>ANIERES</th>
                    <th>LULLY</th>
                    <th>LULLIER</th>
                    <th>BERNEX</th>
                    <th>TROINEX</th>
                    <th>MEINIER</th>
                </tr>
                <tr>
                    <th>time</th>
                    <th></th>
                    <th></th>
                    <th></th>
                    <th></th>
                    <th></th>
                    <th></th>
                    <th></th>
                    <th></th>
                    <th></th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <th>2021-08-13 00:00:00</th>
                    <td>19.3</td>
                    <td>17.8</td>
                    <td>18.5</td>
                    <td>17.9</td>
                    <td>20.6</td>
                    <td>18.4</td>
                    <td>20.3</td>
                    <td>18.6</td>
                    <td>19.4</td>
                    <td>25.8</td>
                </tr>
                <tr>
                    <th>2021-08-13 00:10:00</th>
                    <td>19.6</td>
                    <td>17.9</td>
                    <td>18.4</td>
                    <td>17.7</td>
                    <td>20.0</td>
                    <td>18.3</td>
                    <td>19.6</td>
                    <td>18.7</td>
                    <td>19.1</td>
                    <td>28.6</td>
                </tr>
                <tr>
                    <th>2021-08-13 00:20:00</th>
                    <td>19.0</td>
                    <td>17.7</td>
                    <td>18.2</td>
                    <td>17.6</td>
                    <td>19.4</td>
                    <td>18.4</td>
                    <td>19.1</td>
                    <td>18.7</td>
                    <td>19.2</td>
                    <td>24.1</td>
                </tr>
                <tr>
                    <th>2021-08-13 00:30:00</th>
                    <td>18.3</td>
                    <td>18.0</td>
                    <td>18.1</td>
                    <td>17.4</td>
                    <td>19.1</td>
                    <td>18.3</td>
                    <td>19.1</td>
                    <td>18.6</td>
                    <td>18.9</td>
                    <td>22.5</td>
                </tr>
                <tr>
                    <th>2021-08-13 00:40:00</th>
                    <td>18.7</td>
                    <td>18.0</td>
                    <td>18.1</td>
                    <td>17.6</td>
                    <td>19.1</td>
                    <td>18.0</td>
                    <td>19.0</td>
                    <td>18.7</td>
                    <td>18.5</td>
                    <td>21.5</td>
                </tr>
                <tr>
                    <th>...</th>
                    <td>...</td>
                    <td>...</td>
                    <td>...</td>
                    <td>...</td>
                    <td>...</td>
                    <td>...</td>
                    <td>...</td>
                    <td>...</td>
                    <td>...</td>
                    <td>...</td>
                </tr>
                <tr>
                    <th>2021-08-16 23:10:00</th>
                    <td>17.5</td>
                    <td>17.8</td>
                    <td>17.3</td>
                    <td>16.9</td>
                    <td>17.9</td>
                    <td>17.6</td>
                    <td>17.3</td>
                    <td>17.2</td>
                    <td>17.9</td>
                    <td>22.2</td>
                </tr>
                <tr>
                    <th>2021-08-16 23:20:00</th>
                    <td>17.4</td>
                    <td>17.9</td>
                    <td>17.4</td>
                    <td>17.1</td>
                    <td>17.9</td>
                    <td>17.6</td>
                    <td>17.3</td>
                    <td>17.2</td>
                    <td>18.0</td>
                    <td>22.0</td>
                </tr>
                <tr>
                    <th>2021-08-16 23:30:00</th>
                    <td>17.2</td>
                    <td>17.9</td>
                    <td>17.5</td>
                    <td>17.3</td>
                    <td>17.8</td>
                    <td>17.6</td>
                    <td>17.3</td>
                    <td>17.3</td>
                    <td>18.0</td>
                    <td>21.7</td>
                </tr>
                <tr>
                    <th>2021-08-16 23:40:00</th>
                    <td>17.2</td>
                    <td>17.9</td>
                    <td>17.7</td>
                    <td>17.1</td>
                    <td>17.7</td>
                    <td>17.4</td>
                    <td>17.2</td>
                    <td>17.1</td>
                    <td>18.1</td>
                    <td>21.9</td>
                </tr>
                <tr>
                    <th>2021-08-16 23:50:00</th>
                    <td>17.1</td>
                    <td>17.8</td>
                    <td>17.5</td>
                    <td>17.1</td>
                    <td>17.7</td>
                    <td>17.3</td>
                    <td>17.1</td>
                    <td>17.1</td>
                    <td>18.1</td>
                    <td>22.0</td>
                </tr>
            </tbody>
    </table></div>
    <p>576 rows × 10 columns</p>
</div>

See [the user guide](https://agrometeo-geopy.readthedocs.io/en/latest/usage) for more details.

## Acknowledgements

- This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [zillionare/cookiecutter-pypackage](https://github.com/zillionare/cookiecutter-pypackage) project template.
