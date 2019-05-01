from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

# remaining_field_names = ['street', 'city', 'state', 'tax year', 'taxes owed']
field_names = ['parcel number', 'acres', 'property class', 'full name', 'zip code','taxable value', 'sale date', 'sale amount']

input_file = 'parcels.csv'
output_file = 'skamania.csv'

driver = webdriver.Chrome()
driver.get('http://skamaniawa.taxsifter.com/Assessor.aspx?keyId=186617&parcelNumber=02052000180000&typeID=1')
xpath = '//*[@id="ctl00_cphContent_btnAgree"]'
submit_button = driver.find_element_by_xpath(xpath)
type(submit_button)
submit_button.click()

parcel_number = ""
total_acres = ""
property_class = ""
owner_name = ""
zip_code = ""
taxable_value = ""
sale_date = ""
sale_amount = ""

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
                parcel_number = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_ParcelOwnerInfo1_lbParcelNumber"]').text.encode('utf8')
            except:
                parcel_number = 'N/A'
            
            try:
                total_acres = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_ctl00_dvAssessmentData"]/tbody/tr[4]/td[2]').text.encode('utf8')
            except:
                total_acres = 'N/A'

            try:
                property_class = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_ParcelOwnerInfo1_lbMID1Value"]').text.encode('utf8')
            except:
                property_class = 'N/A'

            try:
                owner_name = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_ParcelOwnerInfo1_lbOwnerName"]').text.encode('utf8')
            except:
                owner_name = 'N/A'

            try:
                zip_code = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_ParcelOwnerInfo1_lbZip"]').text.encode('utf8')
            except:
                zip_code = 'N/A'

            try:
                taxable_value = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_ctl00_dvTaxableValues"]/tbody/tr[4]/td[2]').text.encode('utf8')
            except:
                taxable_value = 'N/A'

            try:
                sale_date = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_ctl02_GridView1"]/tbody/tr[2]/td[1]').text.encode('utf8')
            except:
                sale_date = 'N/A'

            try:
                sale_amount = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_ctl02_GridView1"]/tbody/tr[2]/td[7]').text.encode('utf8')
            except:
                sale_amount = 'N/A'


            writer.writerow({'parcel number': parcel_id_string, 'acres': total_acres, 'property class': property_class, 'full name': owner_name, 'zip code': zip_code, 'taxable value': taxable_value, 'sale date': sale_date, 'sale amount': sale_amount})

            print('parsed: ', parcel_id_string)