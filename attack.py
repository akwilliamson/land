#!/usr/bin/python

import csv
import urllib2
from bs4 import BeautifulSoup
import re

field_names = ['tmk', 'name', 'address', 'state', 'zip', 'class', 'acres', 'assessed value', 'tax year', 'taxes owed']

# Create `records.csv` and write column headers. This file will ultimately store all the filtered records
with open('records.csv', 'w') as records:
    writer = csv.writer(records)
    writer.writerow(field_names)

    with open('tmks.csv', 'r') as tmks_csv:
        tmks = csv.reader(tmks_csv, delimiter=',')

        for tmk in tmks:
            
            data = urllib2.urlopen('http://qpublic9.qpublic.net/hi_hawaii_display.php?county=hi_hawaii&KEY=' + tmk[0])
            soup = BeautifulSoup(data, 'html.parser')
            tables = soup.find_all('table', attrs={'class': 'table_class'})

            # Tax Information
            tax_info = soup.find(string=re.compile('Current Tax Bill Information'))
            table_tax_info = tax_info.find_parent('table')

            # taxes owed
            raw_taxes_owed = table_tax_info.find(lambda tag:tag.name=="b" and "$" in tag.text).text
            taxes_owed = raw_taxes_owed.replace(',','').strip()[1:].strip()
            if float(taxes_owed) == 0.00:
                continue
            print(taxes_owed)

            # tax year
            raw_tax_year = table_tax_info.find('td', {'class': 'sales_value'})
            tax_year = raw_tax_year.text.strip()
            print(tax_year)
