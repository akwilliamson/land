from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

field_names = ['Parcel Number', 'Acres', 'Market Land Value', 'Market Structure Value', 'Net Taxable Value', 'Taxes Due', 'Property Class', 'Owner Address']

input_file = 'parcels.csv'
output_file = 'benton.csv'

driver = webdriver.Chrome()

acres = ""
market_land_value = ""
market_structure_value = ""
net_taxable_value = ""
taxes_due = ""
property_class = ""
owner_name = ""
address_1 = ""
address_2 = ""

with open(output_file, 'w') as records:
    writer = csv.DictWriter(records, fieldnames=field_names)
    writer.writeheader()

    with open(input_file, 'r') as parcels_csv:
        parcel_ids = csv.reader(parcels_csv, delimiter=',')

        for parcel_id in parcel_ids:
            parcel_id_string = str(parcel_id[0])

            url = 'https://www.co.benton.or.us/assessment/property-search-detail?property=' + parcel_id_string
            print 'scraping parcel #: ' + parcel_id_string + ' at: ' + url

            driver.get(url)
        
            try:
                acres = driver.find_element_by_xpath('//*[@id="block-system-main"]/div[2]/div/div[2]/div[1]/div[8]').text.encode('utf8')
            except:
                acres = 'N/A'

            try:
                market_land_value = driver.find_element_by_xpath('//*[@id="block-system-main"]/div[2]/div/div[2]/div[2]/div[3]').text.encode('utf8')
            except:
                market_land_value = 'N/A'

            try:
                market_structure_value = driver.find_element_by_xpath('//*[@id="block-system-main"]/div[2]/div/div[2]/div[2]/div[6]').text.encode('utf8')
            except:
                market_structure_value = 'N/A'

            try:
                net_taxable_value = driver.find_element_by_xpath('//*[@id="block-system-main"]/div[2]/div/div[2]/div[2]/div[21]').text.encode('utf8')
            except:
                net_taxable_value = 'N/A'
            
            try:
                taxes_due = driver.find_element_by_xpath('//*[@id="block-system-main"]/div[2]/div/div[5]/div[2]/div[5]').text.encode('utf8')
            except:
                taxes_due = 'N/A'

            try:
                property_class = driver.find_element_by_xpath('//*[@id="block-system-main"]/div[2]/div/div[2]/div[1]/div[11]').text.encode('utf8')
            except:
                property_class = 'N/A'

            try:
                owner_address = driver.find_element_by_xpath('//*[@id="block-system-main"]/div[2]/div/div[4]/div[1]').text.encode('utf8')
            except:
                owner_address = 'N/A'

            writer.writerow({'Parcel Number': parcel_id_string, 'Acres': acres, 'Market Land Value': market_land_value, 'Market Structure Value': market_structure_value, 'Net Taxable Value': net_taxable_value, 'Taxes Due': taxes_due, 'Property Class': property_class, 'Owner Address': owner_address })

            print('parsed: ', parcel_id_string)