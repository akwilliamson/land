#!/usr/bin/python

# Extract raw parcel data from ARC GIS and parse into sorted TMK lists within CSV files separated by TMK zone

import urllib2
import csv
from operator import itemgetter
import pandas as pd

print('downloading raw data...')

# Download latest GIS data
raw_data = urllib2.urlopen('https://opendata.arcgis.com/datasets/1eb5fa03038d49cba930096ea67194e0_5.csv')

if raw_data.getcode() == 200:
    print('raw data downloaded successfully')
else:
    print('raw data download error. Try again')
    quit()

# Store tmk list
print('extracting tmk values...')
tmks = pd.read_csv(raw_data).tmk
sorted_tmks = sorted(tmks)
print('extraction complete')

# Write each TMK value to `tmk.csv` file, formatted without state code and 4-digit suffix
with open('tmks.csv', 'w') as tmks_file:

    csv_writer = csv.writer(tmks_file)

    print('formatting tmks...')
    for row in sorted_tmks:
        formatted_tmk = str(row)[1:]+'0000'
        csv_writer.writerow([formatted_tmk])

print('formatting complete. all tmks stored in `tmk.csv` file')