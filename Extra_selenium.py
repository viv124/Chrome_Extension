import asyncio
import pandas as pd
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import StaleElementReferenceException

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--search", type=str)
parser.add_argument("-t", "--total", type=int)
args = parser.parse_args()

if args.search:
    search_for = args.search
else:
    search_for = 'Ahmedabad,school'

# Total number of products to scrape. Default is 10
if args.total:
    total = args.total
else:
    total = 3

async def scrape_google_maps():
    l1 = []
    l2 = []
    l3 = []
    l4 = []
    l5 = []

   
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run Chrome in headless mode

   
    webdriver_service = Service('C:/chromedriver_win32/chromedriver.exe')


    chrome_options = webdriver.ChromeOptions()
  
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    wait = WebDriverWait(driver, 5)
    driver.get('https://www.google.com/maps')
    await asyncio.sleep(5)

    search_input = driver.find_element(By.XPATH, '//input[@id="searchboxinput"]')
    search_input.send_keys(search_for)
    await asyncio.sleep(3)

    search_input.send_keys(Keys.RETURN)
    await asyncio.sleep(5)

    l = 0
    while l < total:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        await asyncio.sleep(3)

        listings = driver.find_elements(By.XPATH, '//div[@role="article"]')
        if l >= len(listings):
            break

        try:
            listing = listings[l]
            listing.click()
            await asyncio.sleep(5)

            name_xpath = '//h1[contains(@class,"fontHeadlineLarge")]'
            address_xpath = '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]'
            website_xpath = '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'
            phone_number_xpath = '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]'
            reviews_span_xpath = '//span[@role="img"]'

            name_count = len(driver.find_elements(By.XPATH, name_xpath))
            address_count = len(driver.find_elements(By.XPATH, address_xpath))
            website_count = len(driver.find_elements(By.XPATH, website_xpath))
            phone_number_count = len(driver.find_elements(By.XPATH, phone_number_xpath))
            reviews_span_count = len(driver.find_elements(By.XPATH, reviews_span_xpath))

            name = driver.find_element(By.XPATH, name_xpath).text if name_count > 0 else ''
            address = driver.find_element(By.XPATH, address_xpath).text if address_count > 0 else ''
            website = driver.find_element(By.XPATH, website_xpath).text if website_count > 0 else ''
            phone_number = driver.find_element(By.XPATH, phone_number_xpath).text if phone_number_count > 0 else ''
            reviews = int(driver.find_element(By.XPATH, reviews_span_xpath).get_attribute('aria-label').split()[2].replace(',', '')) if reviews_span_count > 0 else ''

            l1.append(name)
            l2.append(address)
            l3.append(website)
            l4.append(phone_number)
            l5.append(reviews)

            l += 1

        except StaleElementReferenceException:
            # Handle the exception by re-locating the elements
            listings = driver.find_elements(By.XPATH, '//div[@role="article"]')

    data = {
        'name': l1,
        'address': l2,
        'website': l3,
        'phone_number': l4,
        'reviews': l5
    }

    df = pd.DataFrame(data)
    df.to_csv("viv.csv", sep='\t')
    df.to_excel("viv.xlsx")
    print(df)

    driver.quit()

asyncio.run(scrape_google_maps())
