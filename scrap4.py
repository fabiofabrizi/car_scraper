"""
This is just trying to get headless to work
- Specifically, trying to manage the options, so when cookie window pops up:
1. Click 'Manage'
2. Click 'Reject All'
3. Proceed with scraping page
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
option.add_argument('--headless')  # Add this line to enable headless mode
option.add_argument('--no-sandbox')
option.add_argument('--disable-dev-shm-usage')
option.add_argument('--disable-gpu')  # Add this line to disable GPU acceleration
option.add_argument('--disable-extensions')  # Add this line to disable extensions
option.add_experimental_option("excludeSwitches", ["enable-automation"]) # Add this line
# set window size to native GUI size
option.add_argument("--window-size=1920,1080")
option.add_argument("start-maximized")


############  Specify browser driver ######################
driver = webdriver.Chrome(options=option)

def method_3():
    try:
        # Get page HTML through request parse content using BS4
        driver.get(model_url)

        # Wait for the cookie consent button to be clickable and then click it
        wait = WebDriverWait(driver, 7)
        
        # Try different selectors to find the manage button
        button_selectors_manage = [
            (By.ID, 'didomi-notice-learn-more-button'),
            (By.CSS_SELECTOR, '#didomi-notice-learn-more-button'),
            (By.CSS_SELECTOR, 'button[aria-label="Manage"]')

        ]
        manage_button = None
        for selector_type, selector_value in button_selectors_manage:
            try:
                manage_button = wait.until(
                    EC.element_to_be_clickable((selector_type, selector_value))
                )
                break  # If button is found, exit the loop
            except:
                pass  # If button not found with this selector, try the next one
        if manage_button:
            manage_button.click()
            print("On the managing options page")

        sleep(1)
        # Now need to Reject all the cookies
        button_selectors_disagree = [
            (By.ID, 'btn-toggle-disagree'),
            (By.CSS_SELECTOR, '#btn-toggle-disagree'),
            (By.CSS_SELECTOR, 'button[aria-label="Disagree to all: Disagree to our data processing and close"]')
        ]
        disagree_button = None
        for selector_type, selector_value in button_selectors_disagree:
            try:
                disagree_button = wait.until(
                    EC.element_to_be_clickable((selector_type, selector_value))
                )
                break # If button is found, exit loop
            except:
                pass # If button not found with this selector, try next one
        if disagree_button:
            disagree_button.click()
            print("We have disagreed to all the options!!")

        sleep(3)

        results_container = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'results')))
        listings = results_container.find_elements(By.CSS_SELECTOR, '.stock-summary__details')
        print(listings)
        
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

method_3()
overview_model_scraped_data = []
