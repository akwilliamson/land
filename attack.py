#!/usr/bin/python

import csv
import urllib2
from bs4 import BeautifulSoup
import re

field_names = ['tmk', 'name', 'address', 'state', 'zip', 'acres', 'class', 'assessed value', 'tax year', 'taxes owed']

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

            ### ASSESSMENT INFORMATION
            assessment_info = soup.find(string=re.compile('Assessment Information'))
            table_assessment_info = assessment_info.find_parent('table')

            # If the record has more than one property class, skip it
            table_assessment_rows = table_assessment_info.findChildren('tr' , recursive=False)
            if len(table_assessment_rows) > 3:
                continue

            assessment_values = table_assessment_info.findChildren('td', attrs={'class': 'sales_value'})

            ## property class
            property_class = assessment_values[1].text.strip()
            # TODO: SKIP PROPERTY CLASSES IF NOT AGRICULTURAL OR RESIDENTIAL (opt-in possibly homeowner)

            ## assessed building value
            assessed_building_value = assessment_values[-4].text.strip()
            # TODO: SKIP BUILDING VALUES > 0

            ## total taxable value
            total_taxable_value = assessment_values[-1].text.strip()
            # TODO: SKIP VALUES OUTSIDE INPUTTED RANGE (MIN - MAX)

            ### TAX INFORMATION
            tax_info = soup.find(string=re.compile('Current Tax Bill Information'))
            table_tax_info = tax_info.find_parent('table')

            ## taxes owed
            raw_taxes_owed = table_tax_info.find(lambda tag:tag.name=="b" and "$" in tag.text).text
            taxes_owed = raw_taxes_owed.replace(',','').strip()[1:].strip()
            # TODO: SKIP TAXES OWED = 0.00

            ## tax year
            raw_tax_year = table_tax_info.find('td', {'class': 'sales_value'})
            tax_year = raw_tax_year.text.strip()
