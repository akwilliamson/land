from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

field_names = ['Parcel Number', 'Acres', 'Market Value', 'Taxable Value', 'Sale Amount', 'Sale Date', 'Property Class', 'Owner Name']

input_file = 'parcels.csv'
output_file = 'ferry-assessor.csv'

driver = webdriver.Chrome()
driver.get('http://ferrywa.taxsifter.com/Assessor.aspx?keyId=186617&parcelNumber=2038010000001&typeID=1')
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
assessor_button = ""

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
                assessor_button = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_Repeater1_ctl00_pnlResult"]/div[3]/ul/li[1]/a')
            except:
                print  'NOT FOUND: ' + parcel_id_string
                continue
            
            assessor_button.click()

            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_cphContent_ParcelOwnerInfo1_lbParcelNumber"]'))
            )
            
            try:
                acres = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_ctl00_dvAssessmentData"]/tbody/tr[4]/td[2]').text.encode('utf8')
            except:
                acres = 'N/A'

            try:
                market_value = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_ctl00_dvMarketValues"]/tbody/tr[4]/td[2]').text.encode('utf8')
            except:
                market_land_value = 'N/A'

            try:
                taxable_value = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_ctl00_dvTaxableValues"]/tbody/tr[4]/td[2]').text.encode('utf8')
            except:
                taxable_land_value = 'N/A'

            try:
                sale_amount = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_ctl02_GridView1"]/tbody/tr[2]/td[7]').text.encode('utf8')
            except:
                sale_amount = 'N/A'

            try:
                sale_date = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_ctl02_GridView1"]/tbody/tr[2]/td[1]').text.encode('utf8')
            except:
                sale_date = 'N/A'

            try:
                property_class = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_ParcelOwnerInfo1_lbMID1Value"]').text.encode('utf8')
            except:
                property_class = 'N/A'

            try:
                owner_name = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_ParcelOwnerInfo1_lbOwnerName"]').text.encode('utf8')
            except:
                owner_name = 'N/A'

            writer.writerow({'Parcel Number': parcel_id_string, 'Acres': acres, 'Market Value': market_value, 'Taxable Value': taxable_value, 'Sale Amount': sale_amount, 'Sale Date': sale_date, 'Property Class': property_class, 'Owner Name': owner_name })

            print('parsed: ', parcel_id_string)