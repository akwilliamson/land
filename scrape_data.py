#!/usr/bin/python

import urllib2
from bs4 import BeautifulSoup
import csv
import sys

reload(sys)
sys.setdefaultencoding('utf8')

zone_num = input("enter zone #\n")
file_name = 'tmks_zone_' + str(zone_num) + '.csv'
record_file_name = 'records_zone_' + str(zone_num) + '.csv'
base_url = 'http://qpublic9.qpublic.net/hi_hawaii_display.php?county=hi_hawaii&KEY='
field_names = ['tmk', 'name', 'address', 'state', 'zip', 'property class', 'acres', 'market land value', 'assessed building value', 'total taxable value', 'tax year', 'total taxes']

with open(file_name, 'r') as tmk_file:

    with open(record_file_name, 'w') as records:
        dict_writer = csv.DictWriter(records, fieldnames=field_names)
        tmks = csv.reader(tmk_file, delimiter=',')
        dict_writer.writeheader()
        count = 0
        for tmk in tmks:
            count += 1
            url = base_url + tmk[0]
            page = urllib2.urlopen(url)
            html = BeautifulSoup(page, 'html.parser')
            values = [tmk[0]]
            tables = html.find_all('table', attrs={'class': 'table_class'})

            # Extract Owner Information
            if len(tables) == 1:
                print 'record data unavailable for: ' + tmk[0]
            if len(tables) >= 10:
                print 'parsing record ' + str(count) + ': ' + tmk[0]
                owner_info_table = tables[2]

                owner_header_rows = owner_info_table.find_all('td', attrs={'class': 'owner_header'})
                owner_value_rows = owner_info_table.find_all('td', attrs={'class': 'owner_value'})

                for index, owner_header_row in enumerate(owner_header_rows, start = 0):
                    owner_header_text = owner_header_row.text.strip()
                    if owner_header_text == 'Owner Name':
                        values.append(owner_value_rows[index].text.strip())
                    elif owner_header_text == 'Mailing Address':
                        full_address = owner_value_rows[index].text.strip()
                        if len(full_address) > 1:
                            address_components = full_address.split(',')
                            if len(address_components) > 1:
                                place = address_components[0]
                                location = address_components[1].split(' ')
                                state = location[1]
                                zip_code = full_address.split(' ')[-1].strip()
                                values.extend([place, state, zip_code])
                            else:
                                values.extend([address_components, "", ""])
                        else:
                            values.extend(["", "", ""])
                    elif owner_header_text == 'Property Class' or owner_header_text == 'Property Type':
                        values.append(owner_value_rows[index].text.strip())
                    elif owner_header_text == 'Land Area (acres)':
                        values.append(owner_value_rows[index].text.strip())
                    else:
                        pass

                # Extract Assessment Information
                sales_info_table = tables[3]

                sales_header_rows = sales_info_table.find_all('td', attrs={'class': 'sales_header'})
                sales_value_rows = sales_info_table.find_all('td', attrs={'class': 'sales_value'})

                for index, sales_header_row in enumerate(sales_header_rows, start = 0):
                    sales_header_text = sales_header_row.text.strip()
                    
                    if sales_header_text == 'MarketLandValue':
                        text = sales_value_rows[index].text.strip()[1:].strip()
                        values.append(text)
                    elif sales_header_text == 'AssessedBuildingValue':
                        values.append(sales_value_rows[index].text.strip()[1:].strip())
                    elif sales_header_text == 'TotalTaxableValue':
                        values.append(sales_value_rows[index].text.strip()[1:].strip())
                    else:
                        pass


                tax_info_table = tables[10]

                tax_info_data = tax_info_table.find_all('td', attrs={'class': 'sales_value'})
                earliest_year = tax_info_data[0].text.strip()
                back_tax_total = tax_info_data[-2].text.strip()[1:].strip()

                values.append(earliest_year)
                values.append(back_tax_total)

                if values[-1] == '0.00':
                    values[-1] = ""

                if ' 0.00' in values[-2]:
                    values[-2] = ""

                if values[-3] == '0':
                    values[-3] = ""

                if values[-4] == '0':
                    values[-4] = ""
                dict_writer.writerow({'tmk': values[0], 'name': values[1], 'address': values[2], 'state': values[3], 'zip': values[4], 'property class': values[5], 'acres': values[6], 'market land value': values[7], 'assessed building value': values[8], 'total taxable value': values[9], 'tax year': values[10], 'total taxes': values[11]})









