"""
This is to test the functionality of looping over the CSV file and modifying the URL

"""

import csv
import math
from urllib.parse import urlencode, quote

def modify_url(base_url, make, model, size=30):
    """
    Modifies the URL by adding make, model, and size as query parameters.

    Args:
        base_url (str): The base URL to modify.
        make (str): The make of the car.
        model (str): The model of the car.
        size (int, optional): The size parameter. Defaults to 30.

    Returns:
        str: The modified URL.
    """
    params = {
        'make': make,
        'model': model,
        'size': size
    }
    # Use quote_via=quote to encode spaces as %20
    modified_url = base_url + '?' + urlencode(params, quote_via=quote)
    return modified_url
def calculate_pages(number_for_sale):
    """
    Calculates the number of pages based on the number of items for sale.

    Args:
        number_for_sale (int): The number of items for sale.

    Returns:
        int: The number of pages.
    """
    if number_for_sale <= 30:
        return 1
    else:
        return math.ceil(number_for_sale / 30)

def process_csv(input_file, output_file):
    """
    Reads a CSV file, adds a 'modified URL' column, and writes to a new CSV file.

    Args:
        input_file (str): The path to the input CSV file.
        output_file (str): The path to the output CSV file.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as infile, \
             open(output_file, 'w', newline='', encoding='utf-8') as outfile:

            reader = csv.DictReader(infile)
            if not reader.fieldnames:
                print("Error: Input CSV file is empty or has no headers.")
                return

            writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames + ['modified URL', 'pages'])
            writer.writeheader()

            for row in reader:
                make = row['make']
                model = row['name']  # Use 'name' column as the model
                base_url = f"https://www.carzone.ie{row['model URL']}"
                modified_url = modify_url(base_url, make, model)
                number_for_sale = int(row['number for sale'])
                pages = calculate_pages(number_for_sale)

                row['modified URL'] = modified_url
                row['pages'] = pages
                writer.writerow(row)

        print(f"Successfully processed '{input_file}'. Output saved to '{output_file}'.")

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
    except ValueError:
        print("Error: 'number for sale' column contains non-numeric data.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    input_csv_file = 'OO_model_list.csv'  # Replace with your input file name
    output_csv_file = 'OO_model_list_mod.csv'  # Replace with your desired output file name
    process_csv(input_csv_file, output_csv_file)
