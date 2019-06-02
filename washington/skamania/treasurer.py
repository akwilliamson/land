from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

field_names = ['parcel number', 'address 1', 'address 2', 'city', 'state', 'taxes due']

input_file = 'parcels.csv'
output_file = 'skamania.csv'

driver = webdriver.Chrome()
driver.get('http://skamaniawa.taxsifter.com/Assessor.aspx?keyId=186617&parcelNumber=02052000180000&typeID=1')
xpath = '//*[@id="ctl00_cphContent_btnAgree"]'
submit_button = driver.find_element_by_xpath(xpath)
type(submit_button)
submit_button.click()

parcel_number = ""
address_1 = ""
address_2 = ""
city = ""
state = ""
taxes_due = ""

with open(output_file, 'w') as records:
    writer = csv.DictWriter(records, fieldnames=field_names)
    writer.writeheader()

    with open(input_file, 'r') as parcels_csv:
        parcel_ids = csv.reader(parcels_csv, delimiter=',')

        for parcel_id in parcel_ids:
            parcel_id_string = str(parcel_id[0])
            length = len(parcel_id_string)
            
            if len(parcel_id_string) < 14:
                parcel_id_string = '0' + parcel_id_string

            url = 'http://skamaniawa.taxsifter.com/Search/results.aspx?q=' + parcel_id_string
            print 'scraping parcel #: ' + parcel_id_string + ' at: ' + url

            driver.get(url)

            assessor_button = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_Repeater1_ctl00_pnlResult"]/div[3]/ul/li[2]/a')
            type(submit_button)
            assessor_button.click()

            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_cphContent_ParcelOwnerInfo1_lbParcelNumber"]'))
            )
            
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

            try:
                taxes_due = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_CurrentTaxYearInterest1_GridView1"]/tbody/tr[2]/td[8]').text.encode('utf8')
            except:
                taxes_due = '0'

            writer.writerow({'parcel number': parcel_id_string, 'address 1': address_1, 'address 2': address_2, 'city': city, 'state': state, 'taxes due': taxes_due})

            print('parsed: ', parcel_id_string)