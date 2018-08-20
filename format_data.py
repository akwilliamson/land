import os
import csv
import operator

raw_data = 'raw_example.csv'
tmk_data = 'tmks.csv'
tmk_zone = 'tmks_zone_'

# Separate raw parcel data into sorted TMK CSV files, separated by zone
with open(raw_data) as r, open(tmk_data, 'w') as w:

    # Create writer/reader objects
    writer = csv.writer(w)
    reader = csv.reader(r)
    
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