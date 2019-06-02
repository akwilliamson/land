from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

field_names = ['Parcel Number', 'Acres', 'Market Land Value', 'Market Structure Value', 'Net Taxable Value', 'Taxes Due', 'Property Class', 'Owner Name', 'Address 1', 'Address 2']

input_file = 'parcels.csv'
output_file = 'skamania.csv'

driver = webdriver.Chrome()
driver.get('http://skamaniawa.taxsifter.com/Assessor.aspx?keyId=186617&parcelNumber=02052000180000&typeID=1')
xpath = '//*[@id="ctl00_cphContent_btnAgree"]'
submit_button = driver.find_element_by_xpath(xpath)
type(submit_button)
submit_button.click()

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
            length = len(parcel_id_string)
            
            if len(parcel_id_string) < 14:
                continue

            url = 'http://skamaniawa.taxsifter.com/Search/results.aspx?q=' + parcel_id_string
            print 'scraping parcel #: ' + parcel_id_string + ' at: ' + url

            driver.get(url)

            assessor_button = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_Repeater1_ctl00_pnlResult"]/div[3]/ul/li[1]/a')
            type(submit_button)
            assessor_button.click()

            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_cphContent_ParcelOwnerInfo1_lbParcelNumber"]'))
            )
            
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
                owner_name = driver.find_element_by_xpath('//*[@id="block-system-main"]/div[2]/div/div[4]/div[1]/text()[1]').text.encode('utf8')
            except:
                owner_name = 'N/A'

            try:
                address_1 = driver.find_element_by_xpath('//*[@id="block-system-main"]/div[2]/div/div[4]/div[1]/text()[2]').text.encode('utf8')
            except:
                address_1 = 'N/A'

            try:
                address_2 = driver.find_element_by_xpath('//*[@id="block-system-main"]/div[2]/div/div[4]/div[1]/text()[3]').text.encode('utf8')
            except:
                address_2 = 'N/A'

            writer.writerow({'Parcel Number': parcel_id_string, 'Acres': acres, 'Market Land Value': market_value, 'Net Taxable Value': net_taxable_value, 'Taxes Due': taxes_due, 'Property Class': property_class, 'Owner Name': owner_name, 'Address 1': address_1, 'Address 2': address_2 })

            print('parsed: ', parcel_id_string)