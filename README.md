## A brief outline of what the various files do


#### car_scraper_class.py

This implements a scraper using OO methodology.
The class CarZoneScraper takes:
- The base url
- The base used cars url
- Initializes an empty list for the scraped data
- Creates a manufacturer list (from the list of makes)

Functions to:
- Scrape the manufacturer models:
    - make
    - name,
    - model url
    - number for sale
- Start scrape
- Save to CSV

Calls the functions:
- Start scrape
- Save to CSV (model list)
- Save to CSV (manufacturer list)


#### car_scraper_3.py

Currently using a test url - The proper implementation will loop over the 'model_list.csv' file
- The issue with this one was that a cookie button had to be pressed.

#### scrap2.py

This loops over the CSV file and modifies the URL, i.e if the number in the 'pages' column is > 1
then there has to be multiple pages looped over.


To-do:
- Headlesss
- 