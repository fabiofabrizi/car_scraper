"""
This scraper builds on car_scraper_2.py by getting the model url and scraping all the individual car URL's.

What to scrape?
- Individual model link
- Get the number for sale from the model_list.csv
- Remember only a max of 30 per page - so only start with 60 max and randomise time
- Then look at proxies, threading, fake browser headers, etc

What to scrape in car_scraper_4.py?
- Year
- Mileage
- Model
- Price
- Dealer or Private
- Location
- Home delivery (options)
- Online Finance (options)
- Video call/Tour (options)
- Click and Collect (options)
- cartell.ie checked (options)
- Whether it's a featured car


Firstly:
- Import functionality from car_scraper_2.py to test, and keep this clean
- Have in the format {make} {model} which can be extracted from the URL - the last 2 items respectively
"""
import csv
import requests
from bs4 import BeautifulSoup

# Import Selenium as content is rendered Dynamically
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback

from time import sleep

# Initially, just have a test URL.
# The proper thing will loop over the URL's in the 'model_list.csv' file

model_url = 'https://www.carzone.ie/used-cars/bmw/3-series?make=bmw&model=3%20Series'

############  Set options ################################
option = webdriver.ChromeOptions()
#option.add_argument('--headless')
option.add_argument('--no-sandbox')
option.add_argument('--disable-dev-sh-usage')
# set window size to native GUI size
option.add_argument("--window-size=1920,1080")  
option.add_argument("start-maximized")


############  Specify browser driver ######################
driver = webdriver.Chrome(options=option)


############  Getting page HTML through request parse content using BS4

def method_1():
    try:
        ############  Getting page HTML through request parse content using BS4
        driver.get(model_url)

        # Wait for the cookie consent button to be clickable and then click it
        wait = WebDriverWait(driver, 2)
        accept_button = wait.until(
            EC.element_to_be_clickable((By.ID, 'didomi-notice-agree-button'))
        )
        accept_button.click()

        # Wait for a short period to allow the page to load after accepting cookies
        sleep(3)
        wait_5 = WebDriverWait(driver, 5)
        listing_buttons = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'results')))
        #soup = BeautifulSoup(driver.page_source, 'html.parser')
        #sleep(2)
        #models = soup.get('a')
        #models = soup.find_all('.cz-panel a')
        print(listing_buttons.text)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()
    # Where the scraped data goes - This is the listing of all 
    # models

def method_2():
    try:
        driver.get(model_url)

        wait = WebDriverWait(driver, 7)
        accept_button = wait.until(
            EC.element_to_be_clickable((By.ID, 'didomi-notice-agree-button'))
        )
        accept_button.click()

        sleep(3)

        results_container = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'results')))
        model_links = results_container.find_elements(By.TAG_NAME, 'a')  # Find all 'a' tags within the container

        for link in model_links:
            href = link.get_attribute('href')
            model_name = link.text
            print(f"Model: {model_name}, Link: {href}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

def method_3():
    try:
        ############  Getting page HTML through request parse content using BS4
        driver.get(model_url)

        # Wait for the cookie consent button to be clickable and then click it
        wait = WebDriverWait(driver, 7)
        accept_button = wait.until(
            EC.element_to_be_clickable((By.ID, 'didomi-notice-agree-button'))
        )
        accept_button.click()

        sleep(3)

        results_container = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'results')))
        listings = results_container.find_elements(By.CSS_SELECTOR, '.stock-summary__details')

        for listing in listings:
            try:
                # Get general desc
                model_element = listing.find_element(By.CSS_SELECTOR, '.stock-summary__details__header')
                model_name = model_element.text.strip()

                # Get general spec
                details_elements = listing.find_elements(By.CSS_SELECTOR, '.stock-summary__description')
                details = [detail.text.strip() for detail in details_elements]
                
                # Get year, mileage, fuel type
                features_elements = listing.find_elements(By.CSS_SELECTOR,'.stock-summary__features__details')
                features = [feature.text.strip() for feature in features_elements]
                
                # Get type of dealer & location
                dealer_info = listing.find_elements(By.CSS_SELECTOR, '.stock-summary__features__dealer')

                complete_dealer = [item.strip() for comp_dealer in dealer_info for item in comp_dealer.text.replace('\n', ' ').split(' ')] if dealer_info else ''
                dealer = complete_dealer[0]
                location = complete_dealer[1] if len(complete_dealer) > 1 else ''

                # Get link
                model_link = listing.find_elements(By.CSS_SELECTOR, '.cz-panel.stock-summary a')
                if model_link:  # Check if any links were found
                    model_link = model_link[0]  # Get the first WebElement object from the list
                    href = model_link.get_attribute('href')
                else:
                    print("No link found for this listing.")
                


                print("Model:", model_name)
                #print("Link:", model_link)
                print(*details, sep=" • ")  # Print details separated by " • "
                print(*features, sep=" • ")
                print("Type of seller:", dealer)
                print("Location:", location)
                #print("Link:", model_link)
                print("Link:", href)
                print("-" * 20)  # Separator for each listing

            except Exception as inner_e:
                print(f"Error extracting details from a listing: {inner_e}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

method_3()
overview_model_scraped_data = []

