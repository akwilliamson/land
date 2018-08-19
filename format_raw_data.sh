#!/bin/bash

# Extract TMK column only into separate CSV for future use
cut -d ',' -f 2 raw_example.csv > tmp.csv &&
# Move temporary file to formatted file
cat tmp.csv > formatted.csv &&
# Sort the TMKs in order of lowest to highest
sort -k1 -n -t, formatted.csv > tmp.csv &&
# Move temporary file to formatted file
cat tmp.csv > formatted.csv &&
# # Remove first character of each TMK (not used in the qpublic URL query param)
cat formatted.csv | sed 's/^.//' > tmp.csv &&
# Move temporary file to formatted file
cat tmp.csv > formatted.csv &&
# # Append 4 zeros to each TMK (necessary for qpublic URL query param)
sed 's/$/0000/' formatted.csv > tmp.csv &&
# Move temporary file to formatted file
cat tmp.csv > formatted.csv &&
# Remove temporary file
rm rm tmp.csv
