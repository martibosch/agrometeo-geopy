[![PyPI version fury.io](https://badge.fury.io/py/agrometeo-geopy.svg)](https://pypi.python.org/pypi/agrometeo-geopy/)
[![Documentation Status](https://readthedocs.org/projects/agrometeo-geopy/badge/?version=latest)](https://agrometeo-geopy.readthedocs.io/en/latest/?badge=latest)
[![CI/CD](https://github.com/martibosch/agrometeo-geopy/actions/workflows/dev.yml/badge.svg)](https://github.com/martibosch/agrometeo-geopy/blob/main/.github/workflows/dev.yml)
[![codecov](https://codecov.io/gh/martibosch/agrometeo-geopy/branch/main/graph/badge.svg?token=hKoSSRn58a)](https://codecov.io/gh/martibosch/agrometeo-geopy)
[![GitHub license](https://img.shields.io/github/license/martibosch/agrometeo-geopy.svg)](https://github.com/martibosch/agrometeo-geopy/blob/main/LICENSE)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/martibosch/agrometeo-geopy/HEAD?labpath=docs%2Fusage.ipynb)

# agrometeo-geopy

Pythonic interface to access [agrometeo.ch](https://agrometeo.ch) data.

```python
import agrometeo as agm

start_date = "2021-08-13"
end_date = "2021-08-16"

agm_ds = agm.AgrometeoDataset(region="Canton de Genève")
ts_df = agm_ds.get_ts_df(start_date=start_date, end_date=end_date)
ts_df
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>lat_ch</th>
      <th>long_ch</th>
      <th>altitude</th>
      <th>interval</th>
      <th>phone</th>
      <th>email</th>
      <th>into_service_at</th>
      <th>preview_until</th>
      <th>data_until</th>
      <th>...</th>
      <th>bbox_west</th>
      <th>place_id</th>
      <th>osm_type</th>
      <th>osm_id</th>
      <th>lat</th>
      <th>lon</th>
      <th>display_name</th>
      <th>class</th>
      <th>type</th>
      <th>importance</th>
    </tr>
    <tr>
      <th>id</th>
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
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>44</th>
      <td>DARDAGNY</td>
      <td>487462.0</td>
      <td>116662.0</td>
      <td>488</td>
      <td>10</td>
      <td>079 332 38 36</td>
      <td>domaine.les.hutins@bluewin.ch</td>
      <td>2005-11-01</td>
      <td>2022-03-30T14:00:00.000000Z</td>
      <td>2022-03-24T01:00:00.000000Z</td>
      <td>...</td>
      <td>5.955911</td>
      <td>282250030</td>
      <td>relation</td>
      <td>1702419</td>
      <td>46.225651</td>
      <td>6.143921</td>
      <td>Geneva, Switzerland</td>
      <td>boundary</td>
      <td>administrative</td>
      <td>0.550757</td>
    </tr>
    <tr>
      <th>45</th>
      <td>LA-PLAINE</td>
      <td>489447.0</td>
      <td>115605.0</td>
      <td>360</td>
      <td>10</td>
      <td>079 332 32 73</td>
      <td>gegedudu@bluewin.ch</td>
      <td>2005-11-02</td>
      <td>2022-03-30T14:00:00.000000Z</td>
      <td>2022-03-24T01:00:00.000000Z</td>
      <td>...</td>
      <td>5.955911</td>
      <td>282250030</td>
      <td>relation</td>
      <td>1702419</td>
      <td>46.225651</td>
      <td>6.143921</td>
      <td>Geneva, Switzerland</td>
      <td>boundary</td>
      <td>administrative</td>
      <td>0.550757</td>
    </tr>
    <tr>
      <th>46</th>
      <td>SATIGNY</td>
      <td>491847.0</td>
      <td>119767.0</td>
      <td>442</td>
      <td>10</td>
      <td>079 332 36 56</td>
      <td>info@champvigny.ch</td>
      <td>2005-11-01</td>
      <td>2022-03-30T14:00:00.000000Z</td>
      <td>2022-03-24T01:00:00.000000Z</td>
      <td>...</td>
      <td>5.955911</td>
      <td>282250030</td>
      <td>relation</td>
      <td>1702419</td>
      <td>46.225651</td>
      <td>6.143921</td>
      <td>Geneva, Switzerland</td>
      <td>boundary</td>
      <td>administrative</td>
      <td>0.550757</td>
    </tr>
    <tr>
      <th>47</th>
      <td>PEISSY</td>
      <td>489978.0</td>
      <td>118092.0</td>
      <td>450</td>
      <td>10</td>
      <td>079 332 32 81</td>
      <td>lesvallieres@bluewin.ch</td>
      <td>2005-11-03</td>
      <td>2022-03-30T14:00:00.000000Z</td>
      <td>2022-03-24T01:00:00.000000Z</td>
      <td>...</td>
      <td>5.955911</td>
      <td>282250030</td>
      <td>relation</td>
      <td>1702419</td>
      <td>46.225651</td>
      <td>6.143921</td>
      <td>Geneva, Switzerland</td>
      <td>boundary</td>
      <td>administrative</td>
      <td>0.550757</td>
    </tr>
    <tr>
      <th>48</th>
      <td>ANIERES</td>
      <td>506285.0</td>
      <td>125138.0</td>
      <td>412</td>
      <td>10</td>
      <td>079 332 38 89</td>
      <td>vinsvillard@bluewin.ch</td>
      <td>2005-11-03</td>
      <td>2022-03-30T14:00:00.000000Z</td>
      <td>2022-03-24T01:00:00.000000Z</td>
      <td>...</td>
      <td>5.955911</td>
      <td>282250030</td>
      <td>relation</td>
      <td>1702419</td>
      <td>46.225651</td>
      <td>6.143921</td>
      <td>Geneva, Switzerland</td>
      <td>boundary</td>
      <td>administrative</td>
      <td>0.550757</td>
    </tr>
    <tr>
      <th>49</th>
      <td>LULLY</td>
      <td>494821.0</td>
      <td>113788.0</td>
      <td>435</td>
      <td>10</td>
      <td>079 332 36 60</td>
      <td>daniel.tremblet@bluewin.ch</td>
      <td>2005-11-03</td>
      <td>2022-03-30T14:00:00.000000Z</td>
      <td>2021-11-30T06:00:00.000000Z</td>
      <td>...</td>
      <td>5.955911</td>
      <td>282250030</td>
      <td>relation</td>
      <td>1702419</td>
      <td>46.225651</td>
      <td>6.143921</td>
      <td>Geneva, Switzerland</td>
      <td>boundary</td>
      <td>administrative</td>
      <td>0.550757</td>
    </tr>
    <tr>
      <th>52</th>
      <td>LULLIER</td>
      <td>508630.0</td>
      <td>119651.0</td>
      <td>454</td>
      <td>10</td>
      <td></td>
      <td>sebastien.maillard@edu.ge.ch</td>
      <td>2006-01-06</td>
      <td>2022-03-30T14:00:00.000000Z</td>
      <td>2022-03-24T01:00:00.000000Z</td>
      <td>...</td>
      <td>5.955911</td>
      <td>282250030</td>
      <td>relation</td>
      <td>1702419</td>
      <td>46.225651</td>
      <td>6.143921</td>
      <td>Geneva, Switzerland</td>
      <td>boundary</td>
      <td>administrative</td>
      <td>0.550757</td>
    </tr>
    <tr>
      <th>67</th>
      <td>BERNEX</td>
      <td>493900.0</td>
      <td>114060.0</td>
      <td>480</td>
      <td>10</td>
      <td>079 238 60 19</td>
      <td>florian.favre@etat.ge.ch</td>
      <td>2003-01-01</td>
      <td>2022-03-30T14:00:00.000000Z</td>
      <td>2022-01-14T06:00:00.000000Z</td>
      <td>...</td>
      <td>5.955911</td>
      <td>282250030</td>
      <td>relation</td>
      <td>1702419</td>
      <td>46.225651</td>
      <td>6.143921</td>
      <td>Geneva, Switzerland</td>
      <td>boundary</td>
      <td>administrative</td>
      <td>0.550757</td>
    </tr>
    <tr>
      <th>68</th>
      <td>TROINEX</td>
      <td>500520.0</td>
      <td>112865.0</td>
      <td>435</td>
      <td>10</td>
      <td>079 238 59 12</td>
      <td>menetrey@vtx.ch</td>
      <td>2008-06-11</td>
      <td>2022-03-30T14:00:00.000000Z</td>
      <td>2022-03-24T01:00:00.000000Z</td>
      <td>...</td>
      <td>5.955911</td>
      <td>282250030</td>
      <td>relation</td>
      <td>1702419</td>
      <td>46.225651</td>
      <td>6.143921</td>
      <td>Geneva, Switzerland</td>
      <td>boundary</td>
      <td>administrative</td>
      <td>0.550757</td>
    </tr>
    <tr>
      <th>71</th>
      <td>MEINIER</td>
      <td>506270.0</td>
      <td>122120.0</td>
      <td>436</td>
      <td>10</td>
      <td></td>
      <td>menetrey@vtx.ch</td>
      <td>2009-04-07</td>
      <td>2022-03-30T14:00:00.000000Z</td>
      <td>2022-03-23T22:50:00.000000Z</td>
      <td>...</td>
      <td>5.955911</td>
      <td>282250030</td>
      <td>relation</td>
      <td>1702419</td>
      <td>46.225651</td>
      <td>6.143921</td>
      <td>Geneva, Switzerland</td>
      <td>boundary</td>
      <td>administrative</td>
      <td>0.550757</td>
    </tr>
  </tbody>
</table>
<p>10 rows × 32 columns</p>
</div>

See [the user guide](https://agrometeo-geopy.readthedocs.io/en/latest/usage) for more details.

## Acknowledgements

* This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [zillionare/cookiecutter-pypackage](https://github.com/zillionare/cookiecutter-pypackage) project template.
