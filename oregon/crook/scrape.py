#!/usr/bin/env python

import csv
import time
import requests
from bs4 import BeautifulSoup

with open('crook.csv', 'w') as csvfile:
    crook_writer = csv.writer(csvfile, delimiter=',')

    with open('accounts.csv', 'r') as taxlots_csv:
        taxlot_numbers = csv.reader(taxlots_csv, delimiter=',')

        for taxlot_number in taxlot_numbers:

            taxlot_number_string = str(taxlot_number[0])
            
            print('parsing:' + taxlot_number_string)
            
            url = 'http://apps.lanecounty.org/PropertyAssessmentTaxationSearch/crook/Real/Index/' + taxlot_number_string

            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            value_array = []

            left_column = soup.find_all("div", {"id": "uxReportLeftColumn"})
            middle_column = soup.find_all("div", {"id": "uxReportMiddleColumn"})
            right_column = soup.find_all("div", {"id": "uxReportRightColumn"})

            if (not left_column or not middle_column or not right_column):
                continue

            # ************************
            # name and mailing address
            # ************************

            taxlot_number = left_column[0].find_all('span', attrs={'id': 'uxMapTaxlot'})
            value_array.append(taxlot_number[0].text)
            value_array.append(taxlot_number_string)

            for bad_tag in name_and_address_raw[0].find_all(['span', 'img', 'a', 'strong']):
                bad_tag.decompose()

            for br_tag in name_and_address_raw[0].find_all('br'):
                br_tag.replace_with('*')

            name_and_address = name_and_address_raw[0].get_text(strip=True)
            
            value_array.append(name_and_address)

            # ************************
            #    tax, acres, class
            # ************************

            tax_raw = middle_column[0].find_all('strong', text='Property Tax (Current Year):')
            acres_raw = middle_column[0].find_all('strong', text='Assessor Acres:')
            property_class_raw = middle_column[0].find_all('strong', text='Property Class:')

            tax = tax_raw[0].next_sibling.strip()
            acres = acres_raw[0].next_sibling.strip()

            if not property_class_raw:
                print(property_class_raw)
                print("continuing...")
                continue

            property_class = property_class_raw[0].next_sibling.strip()

            value_array.append(tax)
            value_array.append(acres)
            value_array.append(property_class)

            # ************************
            #     property values
            # ************************

            property_values = right_column[0].find_all('td')

            for property_value in property_values:
                string = ""
                value = property_value.text.strip()
                string = value
                value_array.append(string)

            deschutes_writer.writerow(value_array)
