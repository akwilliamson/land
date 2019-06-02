from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

field_names = ['Parcel Number', 'Taxes Due', 'Address 1', 'Address 2', 'City', 'State']

input_file = 'parcels.csv'
output_file = 'ferry-treasurer.csv'

driver = webdriver.Chrome()
driver.get('http://ferrywa.taxsifter.com/Assessor.aspx?keyId=186617&parcelNumber=2038010000001&typeID=1')
xpath = '//*[@id="ctl00_cphContent_btnAgree"]'
submit_button = driver.find_element_by_xpath(xpath)
type(submit_button)
submit_button.click()

parcel_number = ""
taxes_due = ""
address_1 = ""
address_2 = ""
city = ""
state = ""

with open(output_file, 'w') as records:
    writer = csv.DictWriter(records, fieldnames=field_names)
    writer.writeheader()

    with open(input_file, 'r') as parcels_csv:
        parcel_ids = csv.reader(parcels_csv, delimiter=',')
        for i, parcel_id in enumerate(parcel_ids):
            parcel_id_string = str(parcel_id[0])
            length = len(parcel_id_string)

            url = 'http://ferrywa.taxsifter.com/Search/Results.aspx?q=' + parcel_id_string
            print 'scraping: ' + str(i) + ' - parcel: ' + parcel_id_string

            driver.get(url)

            try:
                assessor_button = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_Repeater1_ctl00_pnlResult"]/div[3]/ul/li[2]/a')
                type(submit_button)
                assessor_button.click()
            except:
                continue

            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_cphContent_ParcelOwnerInfo1_lbParcelNumber"]'))
            )
            
            try:
                taxes_due = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_CurrentTaxYearInterest1_GridView1"]/tbody/tr[2]/td[8]').text.encode('utf8')
            except:
                taxes_due = '0'

            try:
                address_1 = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_ParcelOwnerInfo1_lbAddress"]').text.encode('utf8')
            except:
                address_1 = 'N/A'

            try:
                address_2 = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_ParcelOwnerInfo1_lbAddress2"]').text.encode('utf8')
            except:
                address_2 = 'N/A'

            try:
                city = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_ParcelOwnerInfo1_lbCity"]').text.encode('utf8')
            except:
                city = 'N/A'

            try:
                state = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_ParcelOwnerInfo1_lbState"]').text.encode('utf8')
            except:
                state = 'N/A'

            writer.writerow({'Parcel Number': parcel_id_string, 'Taxes Due': taxes_due, 'Address 1': address_1, 'Address 2': address_2, 'City': city, 'State': state })