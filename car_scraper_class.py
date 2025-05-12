"""
This is building on car_scraper_2.py by attempting to use a OO methodology to scrape.

"""

import csv
import requests
from bs4 import BeautifulSoup
# to create a folder to store saved csv files
import os

class CarZoneScraper:
    def __init__(self, base_url='https://www.carzone.ie/', base_used_url='https://www.carzone.ie/used-cars'):
        self.base_url = base_url
        self.base_used_url = base_used_url
        self.scraped_data = []
        self.manufacturer_list = self._create_manufacturer_list()

    def _create_manufacturer_list(self):
        list_of_makes = [
            'audi', 'bmw', 'byd', 'citroen', 'cupra', 'dacia',
            'fiat', 'ford', 'honda', 'hyundai', 'jaguar', 'jeep',
            'kia', 'land-rover', 'lexus', 'mazda', 'mercedes-benz',
            'mg', 'mini', 'mitsubishi', 'nissan', 'opel', 'peugeot',
            'porsche', 'renault', 'seat', 'skoda', 'suzuki', 'tesla',
            'toyota', 'volkswagen', 'volvo'
        ]
        manufacturer_list = []
        for make in list_of_makes:
            manufacturer_list.append({
                'make': make,
                'make_URL': f'{self.base_used_url}/{make}'
            })
        return manufacturer_list

    def _scrape_manufacturer_models(self, url_data):
        response = requests.get(url_data['make_URL'])
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            models = soup.select('.cz-seo-panel__list__item')
            for model in models:
                name = model.select('a')[0].get_text()
                model_name = name.split('(')[0].strip()
                link = model.select('a')[0]
                href = link['href']
                num_for_sale_text = model.select('a span')[0].get_text()
                cleaned_num = int(num_for_sale_text[1:-1].replace(',', ''))

                self.scraped_data.append({
                    'make': url_data['make'],
                    'name': model_name,
                    'model URL': href,
                    'number for sale': cleaned_num
                })

    def start_scrape(self):
        for url_data in self.manufacturer_list:
            self._scrape_manufacturer_models(url_data)

    def save_to_csv(self, data_list, filename):
        assets_folder = 'assets'
        if not data_list:
            print(f"No data to save to {assets_folder}/{filename}.csv")
            return
        keys = data_list[0].keys()
        # Check whether the 'assets folder' exists - if not, create it.
        if not os.path.exists(assets_folder):
            os.makedirs(assets_folder)
        filepath = os.path.join(assets_folder, filename + '.csv')
        with open(filepath, 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data_list)
        print(f"Data saved to {assets_folder}/{filename}.csv")

if __name__ == "__main__":
    scraper = CarZoneScraper()
    scraper.start_scrape()
    scraper.save_to_csv(scraper.scraped_data, 'OO_model_list')
    scraper.save_to_csv(scraper.manufacturer_list, 'OO_manufacturer_list')