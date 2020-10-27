import os
import csv
import logging
import argparse
import requests

from bs4 import BeautifulSoup

wiki_url = 'https://en.wikipedia.org/wiki/List_of_shopping_malls_in_Singapore'
raw_dir = os.path.join(os.getcwd(), 'data', 'raw')

# logging basic configuration
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S',
                    filemode='w')

def main(url):
    # Retrieve the page and pipe into BeautifulSoup
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    # Find the HTML for all regions
    malls = []
    sections = soup.find_all(class_='div-col columns column-width')
    for sec in sections:

        # Find the HTML for malls under each region
        malls_elem = sec.find_all('li')

        for elem in malls_elem:
            mall = elem.text

            # Quick & Fast Cleaning
            mall.replace('[1]', '')
            mall.replace('[2]', '')
            mall = mall[: mall.index('(')] if '(' in mall else mall

            malls.append(mall)

            logging.debug(mall)

    logging.info(f"Number of Malls: {len(malls)}")

    # Write to CSV
    headers = ['name']
    with open(os.path.join(raw_dir, 'shopping-malls.csv'), 'w') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        for mall in malls:
            csvwriter.writerow([mall])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-debug", action="store_true",
                        help="Enable debug mode")

    args = parser.parse_args()
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    main(wiki_url)