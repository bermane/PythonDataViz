
# load packages
import geopandas as gpd
import matplotlib.pyplot as plt
import os
import pandas as pd
import requests

# set folders
data_folder = 'data'
output_folder = 'output'

# define download function


def download(url):
    filename = os.path.join(data_folder, os.path.basename(url))
    if not os.path.exists(filename):
        with requests.get(url, stream=True, allow_redirects=True) as r:
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print('Downloaded', filename)


# download census shapefile and pop stats
shapefile_name = 'tl_2019_06_tract'
shapefile_exts = ['.shp', '.shx', '.dbf', '.prj']
data_url = 'https://github.com/spatialthoughts/python-dataviz-web/releases/' \
    'download/census/'

for ext in shapefile_exts:
    url = data_url + shapefile_name + ext
    download(url)

csv_name = 'ACSST5Y2019.S0101_data.csv'
download(data_url + csv_name)

# read shapefile
shapefile_path = os.path.join(data_folder, shapefile_name + '.shp')
tracts = gpd.read_file(shapefile_path)
tracts.info()

# read csv
csv_path = os.path.join(data_folder, csv_name)
table = pd.read_csv(csv_path, skiprows=[1])
table.info()

# check geoid columns for join
tracts['GEOID'][:5]
table['GEO_ID'][:5]

# clean table data
filtered = table[['GEO_ID', 'NAME', 'S0101_C01_001E']].rename(
    columns={'S0101_C01_001E': 'Population', 'GEO_ID': 'GEOID'})
filtered['GEOID'] = filtered.GEOID.str[-11:]

# recheck columns
# check geoid columns for join
tracts['GEOID'][:5]
filtered['GEOID'][:5]

# merge tables
gdf = tracts.merge(filtered, on='GEOID')

# create density columns
gdf['density'] = 1e6 * gdf['Population'] / gdf['ALAND']

# plot file
fig, ax = plt.subplots(1, 1)
fig.set_size_inches(10, 10)
gdf.plot(ax=ax)
plt.show()

# change fill and edge colors
fig, ax = plt.subplots(1, 1)
fig.set_size_inches(10, 10)
gdf.plot(ax=ax, facecolor='#f0f0f0', edgecolor='#de2d26', linewidth=0.5)

plt.show()

# plot density
fig, ax = plt.subplots(1, 1)
fig.set_size_inches(10, 10)
gdf.plot(ax=ax, column='density', cmap='RdYlGn_r', scheme='quantiles')
plt.show()


# create our own density bins
fig, ax = plt.subplots(1, 1)
fig.set_size_inches(10, 10)

classification_kwds = {
    'bins': [1, 10, 25, 50, 100, 250, 500, 1000, 5000]
}
gdf.plot(ax=ax, column='density', cmap='RdYlGn_r', scheme='User_Defined',
         classification_kwds=classification_kwds, legend=True)

plt.show()

# add legend
legend_kwds = {
    'loc': 'upper right',
    'bbox_to_anchor': (0.8, 0.9),
    'fmt': '{:<5.0f}',
    'frameon': False,
    'fontsize': 8,
    'title': 'persons/sq.km.'
}
classification_kwds = {
    'bins': [1, 10, 25, 50, 100, 250, 500, 1000, 5000]
}

fig, ax = plt.subplots(1, 1)
fig.set_size_inches(10, 10)
gdf.plot(ax=ax, column='density', cmap='RdYlGn_r', scheme='User_Defined',
         classification_kwds=classification_kwds,
         legend=True, legend_kwds=legend_kwds)

ax.set_axis_off()

# Change the last entry in the legend to '>5000'
legend = ax.get_legend()
legend.texts[-1].set_text('> 5000')

plt.show()

# add a title and save
legend_kwds = {
    'loc': 'upper right',
    'bbox_to_anchor': (0.8, 0.9),
    'fmt': '{:<5.0f}',
    'frameon': False,
    'fontsize': 8,
    'title': 'persons/sq.km.'
}
classification_kwds = {
    'bins': [1, 10, 25, 50, 100, 250, 500, 1000, 5000]
}

fig, ax = plt.subplots(1, 1)
fig.set_size_inches(10, 10)
gdf.plot(ax=ax, column='density', cmap='RdYlGn_r', scheme='User_Defined',
         classification_kwds=classification_kwds,
         legend=True, legend_kwds=legend_kwds)

ax.set_axis_off()

# Change the last entry in the legend to '>5000'
legend = ax.get_legend()
legend.texts[-1].set_text('> 5000')

# Add a title
ax.set_title('California Population Density (2019)', size=18)

output_path = os.path.join(output_folder, 'california_pop.png')
plt.savefig(output_path, dpi=300)

plt.show()

# plot sf
fig, ax = plt.subplots(1, 1)
fig.set_size_inches(7, 7)
ax.set_xlim(-122.53, -122.36)
ax.set_ylim(37.71, 37.82)
tracts.plot(ax=ax, facecolor='none')
plt.show()
