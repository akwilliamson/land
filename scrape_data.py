import urllib2
from bs4 import BeautifulSoup

url = 'http://qpublic9.qpublic.net/hi_hawaii_display.php?county=hi_hawaii&KEY=950260110000'
page = urllib2.urlopen(url)
html = BeautifulSoup(page, 'html.parser')

values = []

tables = html.find_all('table', attrs={'class': 'table_class'})

# Extract Owner Information
owner_info_table = tables[2]

owner_header_rows = owner_info_table.find_all('td', attrs={'class': 'owner_header'})
owner_value_rows = owner_info_table.find_all('td', attrs={'class': 'owner_value'})

for index, owner_header_row in enumerate(owner_header_rows, start = 0):
    owner_header_text = owner_header_row.text.strip()
    
    if owner_header_text == 'Owner Name':
        values.append(owner_value_rows[index].text.strip())
    elif owner_header_text == 'Mailing Address':
    	full_address = owner_value_rows[index].text.strip()
    	address_components = full_address.split(',')
    	place = address_components[0]
    	location = address_components[1].split(' ')
    	state = location[1]
    	zip_code = location[2]
        values.extend([place, state, zip_code])
    elif owner_header_text == 'Property Class':
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

if '$' not in values[-2]:
    pass
else:
    values[-2] = 'N/A'

for value in values:
    print(value)













