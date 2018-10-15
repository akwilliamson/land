#!/usr/bin/python

import csv
import urllib2
from bs4 import BeautifulSoup
import re
import unicodedata
import sys

field_names = ['tmk', 'acres', 'property class', 'first name', 'last name', 'street', 'city', 'state', 'zip code', 'taxable value', 'tax year', 'taxes owed']

state_abbreviations = ['AL', 'AK', 'AS', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FM', 'FL', 'GA', 'GU', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MH', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'MP', 'OH', 'OK', 'OR', 'PW', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VI', 'VA', 'WA', 'WV', 'WI', 'WY' ]

total = 0

zone = raw_input("pick a zone number to attack (1-9):\n").strip()
should_filter_homeowner = raw_input("do you want to filter out parcels with a 'HOMEOWNER' property class? y/n\n").strip()
should_filter_buildings = raw_input("do you want to filter out parcels that contain 'assessed building value'? y/n\n").strip()

should_filter_taxable_range = raw_input("do you want to include parcels with a certain 'total taxable value' range? y/n\n").strip()
taxable_range_minimum = ''
taxable_range_maximum = ''

if should_filter_taxable_range.lower() == 'y':
    taxable_range_minimum = raw_input("ignore parcels with a 'total taxable value' less than :\n").strip()
    taxable_range_maximum = raw_input("ignore parcels with a 'total taxable value' greater than:\n").strip()

should_filter_back_taxes = raw_input("do you want to filter out parcels that don't owe back taxes? y/n\n").strip()
back_tax_minimum = ''
back_tax_maximum = ''

if should_filter_back_taxes.lower() == 'y':
    back_tax_minimum = raw_input("ignore parcels with back taxes owed that are less than :\n").strip()
    back_tax_maximum = raw_input("ignore parcels with back taxes owed that are greater than:\n").strip()

def is_valid_zip(value):
  try:
    float(value) and len(value) == 5
    return True
  except:
    return False

def drawProgressBar(percent, barLen = 20):
    sys.stdout.write("\r")
    progress = ""
    for i in range(barLen):
        if i < int(barLen * percent):
            progress += "="
        else:
            progress += " "
    sys.stdout.write("[ %s ] %.3f%%" % (progress, percent * 100))
    sys.stdout.flush()

zone_file = 'tmks_zone_' + zone + '.csv'

with open(zone_file, 'r') as tmks_csv:
    tmks = csv.reader(tmks_csv, delimiter=',')
    total = len(list(tmks))

# Create `records.csv` and write column headers. This file will ultimately store all the filtered records
filename = 'records_zone_' + zone + '.csv'
with open(filename, 'w') as records:

    writer = csv.DictWriter(records, fieldnames=field_names)
    writer.writeheader()

    with open(zone_file, 'r') as tmks_csv:
        tmks = csv.reader(tmks_csv, delimiter=',')

        count = 0

        for tmk in tmks:
            
            # get HTML for tmk record
            data = urllib2.urlopen('http://qpublic9.qpublic.net/hi_hawaii_display.php?county=hi_hawaii&KEY=' + tmk[0])
            soup = BeautifulSoup(data, 'html.parser')
            tables = soup.find_all('table', attrs={'class': 'table_class'})

            count += 1
            percent = (float(count)/total)
            drawProgressBar(percent)

### OWNER AND PARCEL INFORMATION

            contact_info = soup.find(string=re.compile('Owner and Parcel Information'))
            table_contact_info = contact_info.find_parent('table')
            
            contact_values = table_contact_info.findChildren('td', attrs={'class': 'owner_value'})

            # acres
            acres = contact_values[-3].string.strip()

            raw_address = contact_values[2].text.strip()

            # if address doesn't exist, skip parsing and move to the next record
            if raw_address == '':
                continue

            # split address's zip code
            raw_address_components = raw_address.rsplit(' ', 1)
            zip_code = raw_address_components[-1].split('-')[0]

            # if the zip code is invalid, skip parsing and move to the next record
            if is_valid_zip(zip_code) == False:
                continue

            # pop zip code, split address's state abbreviation
            raw_address_components = raw_address_components[:-1]
            state_abbreviation = raw_address_components[0].rsplit(' ', 1)[-1]
            
            # if state abbreviation is invalid, skip parsing and move to the next record
            if state_abbreviation not in state_abbreviations:
                continue

            # pop state abbreviation
            raw_address_components = unicodedata.normalize('NFKC', raw_address_components[0]).rsplit(' ', 1)[:-1]

            street = ''
            city = ''

            # We are going to parse the most common address styles
            if re.match('PO BOX', raw_address_components[0]):
                street = re.match('^[\bPO BOX\b+\d]+(\s)+', raw_address_components[0]).group(0)
                city = re.split('^[\bPO BOX\b+\d]+(\s)+', raw_address_components[0])[-1].strip(',')
            else:
                comps = raw_address_components[0].strip(',').rsplit(' ', 1) 
                street = comps[0]
                city = comps[-1]
            
            # ## owner name
            raw_full_owner_name = contact_values[0].text.strip()
            full_owner_name = raw_full_owner_name.split('Fee Owner',1)[0].strip()
            
            name_components = full_owner_name.split(',',1)
            
            last_name = ''
            first_name = ''

            if len(name_components) > 1:
                last_name = name_components[0]
                first_name = name_components[1]
            else:
                first_name = name_components[0]

            if (first_name.upper() == 'UNITED STATES OF AMERICA') or (first_name.upper() == 'STATE OF HAWAII'):
                continue

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
            if should_filter_homeowner.lower() == 'n':
                if (property_class != 'AGRICULTURAL') and (property_class != 'RESIDENTIAL') and (property_class != 'HOMEOWNER'):
                    continue
            elif (property_class != 'AGRICULTURAL') and (property_class != 'RESIDENTIAL'):
                continue

            ## assessed building value
            assessed_building_value = assessment_values[-4].text.strip()
            formatted_assessed_building_value = assessed_building_value.strip('$').strip()
            if (formatted_assessed_building_value != '0') and (should_filter_buildings.lower() == 'y'):
                continue

            ## total taxable value
            total_taxable_value = assessment_values[-1].text.strip().strip('$').strip().replace(',','')
            if (float(total_taxable_value) < float(taxable_range_minimum)) or (float(total_taxable_value) > float(taxable_range_maximum)):
                continue

### TAX INFORMATION

            tax_info = soup.find(string=re.compile('Current Tax Bill Information'))
            table_tax_info = tax_info.find_parent('table')

            ## tax year
            raw_tax_year = table_tax_info.find('td', {'class': 'sales_value'})
            tax_year = raw_tax_year.text.strip().strip('$').strip()
            if tax_year == '0.00':
                continue

            ## taxes owed
            raw_taxes_owed = table_tax_info.find(lambda tag:tag.name=="b" and "$" in tag.text).text
            taxes_owed = raw_taxes_owed.replace(',','').strip()[1:].strip()
            if should_filter_back_taxes.lower() == 'y':
                if (float(taxes_owed) < float(back_tax_minimum)) or (float(taxes_owed) > float(back_tax_maximum)):
                    continue

            writer.writerow({'tmk': str(tmk[0]), 'acres': acres, 'property class': property_class, 'first name': first_name, 'last name': last_name, 'street': street, 'city': city, 'state': state_abbreviation, 'zip code': zip_code, 'taxable value': total_taxable_value, 'tax year': tax_year, 'taxes owed': taxes_owed})