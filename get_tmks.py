#!/usr/bin/python

import urllib2
import os
import csv
import operator

tmk_data = 'tmks.csv'
tmk_zone = 'tmks_zone_'
gis_url = 'https://opendata.arcgis.com/datasets/1eb5fa03038d49cba930096ea67194e0_5.csv'

# Separate raw parcel data into sorted TMK CSV files, separated by zone
with open(tmk_data, 'w') as w:

	# Download latest GIS data
    r = urllib2.urlopen(gis_url)

    # Create writer/reader objects
    reader = csv.reader(r)
    writer = csv.writer(w)
    
    # Write each TMK value to CSV, formatted w/out state code and 4-digit suffix
    sortedlist = sorted(reader, key=operator.itemgetter(1), reverse=False)
    for row in sortedlist:
        writer.writerow([row[1][1:]+'0000'])

    # 
    with open (tmk_data) as f:
        r = f.readlines()

    for i in range(len(r)):
        row = r[i]
        number = r[i].split(',')[0][0]
        filename = tmk_zone + number + ".csv"
        with open(filename,'a') as f:
            f.write(row)
