# unhcrDataAnalysis
 This repository contains Python code for the extraction and analysis of [United Nations High Commissioner for Refugees data](https://data.unhcr.org/en/situations/mediterranean) about refugee situations in the Mediterranean Sea.
 Refugees Operational Data Portal by UNHCR is licensed under a [Creative Commons Attribution 3.0 International License](https://creativecommons.org/licenses/by/3.0/igo/).
 
 ## Tables
 The code produces the following four tables:


### data.csv
It contains the most information extracted from UNHCR about the disembarkment place of refugees.


| Variable                         | Description|
|:---------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `geomaster_name`                    | Disembarkment place                                                     |
| `admin_level`                      | Administrative level, either Settlement, Province or Country |
| `centroid_lon`             | Longitude of disembarkment place                                      |
| `centroid_lat`        | Latitude of disembarkment place                                |
| `month`          | Month cumulative yearly figures refer to                                  |
| `year` | Year figures refer to                |
| `population_groups_concat` | Population groups figures refer to                |
| `individuals` | Number of disembarked refugees               |
| `country_name` | Country where refugees disembarked                 |
| `last_update` | Date of last update                 |

### data_country_year.csv
It contains aggregated values by country and by year.
| Variable                         | Description|
|:---------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `country_name` | Country where refugees disembarked                 |
| `year` | Year figures refer to                |
| `individuals` | Number of disembarked refugees               |

### data_country.csv
It contains aggregated values by country.
| Variable                         | Description|
|:---------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `country_name` | Country where refugees disembarked                 |
| `individuals` | Number of disembarked refugees               |


### data_year.csv
It contains aggregated values by year.
| Variable                         | Description|
|:---------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `year` | Year figures refer to                |
| `individuals` | Number of disembarked refugees               |


## Visualizations
The code additionally produces visualizations about total refugees disembarked 
 - by country, 
 - by year, 
 - by county and by year
 
and a map for yeach country with the location of the disembarkment places.

Finally, an interactive visualization is produced and opened in browser.


## Author
[Vittorio Nicoletta](https://twitter.com/vi__enne)
