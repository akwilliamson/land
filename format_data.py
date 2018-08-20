import os
import csv
import operator

# Copy the raw daya TMK column into a separate CSV with sorted TMKs
with open('raw_example.csv') as r, open('tmk.csv', 'w') as w:
    # Create writer/reader objects
    writer = csv.writer(w)
    reader = csv.reader(r)
    
    # Write each TMK value
    sortedlist = sorted(reader, key=operator.itemgetter(1), reverse=False)
    for row in sortedlist:
        writer.writerow([row[1]])
