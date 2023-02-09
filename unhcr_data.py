# -*- coding: utf-8 -*-
"""
Analysis of refugees and migrants situation in the Mediterranean Sea
Data source: United Nations High Commissioner for Refugees
Author: V. Nicoletta @vi__enne
"""

# Import packages
import pandas as pd
import geopandas as gpd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from urllib.request import urlopen
import json
import plotly.express as px
import plotly.io as pio
pio.renderers.default = 'browser'

# Parameters
startY = 2014
endY = 2022

# Define function to read data from source and transorm them


def read_and_tranform(geo_id, year):
    url = "https://data.unhcr.org/population/get/sublocation?&geo_id=" + \
        str(geo_id) + "&year=" + str(year) + "&sv_id=11&population_group=4797"
    response = urlopen(url)
    data_json = json.loads(response.read())
    df = pd.json_normalize(data_json['data'])
    if 'individuals' in df.columns:
        df = df.astype({'individuals': 'int'})
        df = df[['geomaster_name', 'admin_level', 'centroid_lon',
                 'centroid_lat', 'date', 'month', 'year',
                 'population_groups_concat', 'individuals']]
        df['geo_id'] = geo_id
    return df


# Initialize arrays and dataframes
year = np.arange(startY, endY+1, 1)
geo_id = np.array([656, 640, 729, 616, 690])
country_names = np.array(['Italy', 'Greece', 'Spain', 'Cyprus', 'Malta'])
countries = {'country_name': country_names,
             'geo_id': geo_id}
countries_df = pd.DataFrame(data=countries)
data = pd.DataFrame()

# Extract data for each country and for each year
for i in geo_id:
    for j in year:
        temp = read_and_tranform(i, j)
        data = pd.concat([data, temp], ignore_index=True)

# Add country name based on geo_id
data = pd.merge(data, countries_df)

# Convert column and drop
data['last_update'] = pd.to_datetime(data['date'])
data['centroid_lat'] = pd.to_numeric(data['centroid_lat'])
data['centroid_lon'] = pd.to_numeric(data['centroid_lon'])
data['year'] = pd.to_numeric(data['year'])
data = data.drop(columns=['date', 'geo_id'])

# Summarize by country and by year
data_country_year = data.groupby(['country_name', 'year'])[
    'individuals'].sum().reset_index()
data_year = data.groupby(['year'])['individuals'].sum().reset_index()
data_country = data.groupby(['country_name'])[
    'individuals'].sum().reset_index()

# Save in .csv format
data.to_csv('output/data.csv', index=False)
data_country_year.to_csv(
    'output/data_country_year.csv', index=False)
data_year.to_csv(
    'output/data_year.csv', index=False)
data_country.to_csv(
    'output/data_country.csv', index=False)

data_country_year_wide = pd.pivot(
    data_country_year, index='year', columns='country_name',
    values='individuals')

# Plots
matplotlib.rcParams.update({'font.size': 6})

plot = data_country.sort_values('individuals', ascending=True).plot.barh(
    'country_name', 'individuals', rot=0, legend=False)
plot.set_title("Refugees disembarked via the Mediterranean Route \n from " +
               str(startY) + " to " + str(endY) + " by arrival country",
               y=0.99,
               fontsize=10)
plot.set_ylabel("Arrival country")
plot.set_xlabel("Individuals")
plot.get_xaxis().set_major_formatter(
    matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
fig = plot.get_figure()
fig.savefig('output/plot_country.png', dpi=300)

plot = data_year.plot.bar('year', 'individuals', rot=0, legend=False)
plot.set_title("Refugees disembarked via the Mediterranean Route \n from " +
               str(startY) + " to " + str(endY) + " by year",
               y=0.99,
               fontsize=10)
plot.set_xlabel("Year")
plot.set_ylabel("Individuals")
plot.get_yaxis().set_major_formatter(
    matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
fig = plot.get_figure()
fig.savefig('output/plot_year.png', dpi=300)

plot = data_country_year_wide.plot.bar(rot=0, stacked=True, colormap="viridis")
plot.set_title("Refugees disembarked via the Mediterranean Route \n from " +
               str(startY) + " to " + str(endY) + " by year",
               y=0.99,
               fontsize=10)
plot.legend(title="Arrival country")
plot.set_xlabel("Year")
plot.set_ylabel("Individuals")
plot.get_yaxis().set_major_formatter(
    matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
fig = plot.get_figure()
fig.savefig('output/plot_country_year.png',
            dpi=300)

# Plot maps
countries = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

for i in country_names:
    fig, ax = plt.subplots(figsize=(8, 6))
    if i == 'Malta':
        countries[countries["name"] == 'Italy'].plot(color="lightgrey", ax=ax)
    else:
        countries[countries["name"] == i].plot(color="lightgrey", ax=ax)
    subdata = data.loc[data["country_name"] == i]
    subdata['size'] = subdata['individuals'].div(100)
    plot = subdata.plot(x="centroid_lon",
                        y="centroid_lat",
                        kind="scatter",
                        s="size",
                        c="year",
                        colormap="Blues",
                        alpha=0.5,
                        title="Refugees disembarked via the Mediterranean Route from " +
                        str(startY) + " to " + str(endY) + " in " + str(i),
                        ax=ax)
    plt.xlabel('')
    plt.ylabel('')
    ax.grid(visible=True, alpha=0.5)
    plt.savefig('output/plot_'+i+'.png', dpi=300)

# Interactive visualization in browser
fig = px.scatter_geo(data, lat="centroid_lat", lon="centroid_lon",
                     hover_name="geomaster_name", size="individuals",
                     color="country_name",
                     animation_frame="year",
                     labels={'country_name': 'Arrival country'},
                     projection="natural earth",
                     # scope="europe",
                     title="Refugees disembarked via the Mediterranean Route from " +
                     str(startY) + " to " + str(endY) + " by destination and by year")
fig.show()
