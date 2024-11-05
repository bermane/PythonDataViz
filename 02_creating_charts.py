# import libraries
import matplotlib.pyplot as plt
import os
import pandas as pd
import requests

# define folders
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

# download files
files = [
  '2020-01-metropolitan-street.csv',
  '2020-02-metropolitan-street.csv',
  '2020-03-metropolitan-street.csv',
  '2020-04-metropolitan-street.csv',
  '2020-05-metropolitan-street.csv',
  '2020-06-metropolitan-street.csv',
  '2020-07-metropolitan-street.csv',
  '2020-08-metropolitan-street.csv',
  '2020-09-metropolitan-street.csv',
  '2020-10-metropolitan-street.csv',
  '2020-11-metropolitan-street.csv',
  '2020-12-metropolitan-street.csv'
]


data_url = 'https://github.com/spatialthoughts/python-dataviz-web/releases/' \
  'download/police.uk/'

for f in files:
  url = os.path.join(data_url + f)
  download(url)

# merge csvs into a single dataframe
dataframe_list = []

for f in files:
    filepath = os.path.join(data_folder, f)
    df = pd.read_csv(filepath)
    dataframe_list.append(df)

merged_df = pd.concat(dataframe_list)

# group by crime type
type_counts = merged_df.groupby('Crime type').size()
type_counts

# pie chart by crime type
fig, ax = plt.subplots(1, 1)
fig.set_size_inches(15,10)
type_counts.plot(kind='pie', ax=ax)
plt.show()

# customize chart
fig, ax = plt.subplots(1, 1)
fig.set_size_inches(15,10)

type_counts.plot(kind='pie', ax=ax)

ax.set_title('Crime Types', fontsize = 18)
ax.set_ylabel('')

plt.tight_layout()
plt.show()

# endless customization
wedgeprops={'linewidth': 3, 'edgecolor': 'white'}
textprops= {'fontsize': 10, 'fontstyle': 'italic'}

fig, ax = plt.subplots(1, 1)
fig.set_size_inches(15,10)

type_counts.plot(kind='pie', ax=ax,
                 wedgeprops=wedgeprops,
                 textprops=textprops
                 )

ax.set_title('Crime Types', fontsize = 18)
ax.set_ylabel('')

plt.tight_layout()
plt.show()

# group data by monthly crime
monthly_counts = merged_df.groupby('Month').size()
monthly_counts

# plot crime by month
fig, ax = plt.subplots(1, 1)
fig.set_size_inches(15,7)
monthly_counts.plot(kind='bar', ax=ax)
plt.show()

# add a line to the bar chart
fig, ax = plt.subplots(1, 1)
fig.set_size_inches(15,7)

monthly_counts.plot(kind='bar', ax=ax)
monthly_counts.plot(kind='line', ax=ax, color='red', marker='o')

ax.set_title('Total Crime by Month')
ax.set_ylabel('Total Incidents')

plt.show()

# plot bike thefts as a line chart
bike_thefts = merged_df[merged_df['Crime type'] == 'Bicycle theft']
bike_thefts

# group by month
bike_thefts_month = bike_thefts.groupby('Month').size()
bike_thefts_month

# plot as line chart
fig, ax = plt.subplots(1, 1)
fig.set_size_inches(15, 7)
bike_thefts_month.plot(kind='line', color='red', marker='o')
ax.set_title('Bicycle Thefts by Month')
ax.set_ylabel('Total Incidents')
plt.show()

# use seaborn style
import seaborn as sns
import numpy as np
sns.set_theme()

fig, ax = plt.subplots(1, 1)
fig.set_size_inches(12,6)
bars = monthly_counts.plot(kind='bar', ax=ax)

ax.set_title('Total Crime by Month (Seaborn Style)', loc='left', pad=20)
ax.set_xlabel('')
ax.set_ylabel('Total Incidents')
ax.set_xticks(np.arange(len(monthly_counts)))

# Extra: Add labels on bars
for bar in bars.patches:
    height = bar.get_height()
    ax.annotate(
        height,
        xy=(bar.get_x() + bar.get_width() / 2, height),
        xytext=(0, 10),
        fontsize=8,
        textcoords="offset points", ha='center', va='bottom',
        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round'))

# Extra: Custmize X-Axis labels

labels = []
for date in pd.to_datetime(monthly_counts.index):
  labels.append(date.strftime('%b'))
ax.set_xticklabels(labels)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()

output_path = os.path.join(output_folder, 'seaborn.png')
plt.savefig(output_path, dpi=300)

plt.show()