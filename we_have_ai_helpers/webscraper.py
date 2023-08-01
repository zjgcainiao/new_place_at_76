import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import re
from datetime import datetime, timedelta

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def scrape_and_download_pdfs():
    base_url = 'https://www.federalreserve.gov/data/sloos/sloos-202307.htm'
    # "https://www.federalreserve.gov/data/sloos.htm"

    # Send a GET request
    response = requests.get(base_url)

    # If the GET request is successful, the status code will be 200
    if response.status_code == 200:
        # Get the content of the response
        page_content = response.content
        # Create a BeautifulSoup object and specify the parser
        soup = BeautifulSoup(page_content, 'html.parser')
        
        # Find the last updated date
        date_string = soup.find('div', class_='lastUpdate', id='lastUpdate').text
        date_string = re.search(r'\b(\w+\s\d{1,2},\s\d{4})\b', date_string)[0]  # adjust this regex according to the date format on the site

        # Convert it to a datetime object
        date = datetime.strptime(date_string, '%B %d, %Y')

        # Get the month before the last updated month
        month_before = date - timedelta(days=30)
        month_before_string = month_before.strftime('%B')
        # Find all pdf links
        pdf_links = soup.select("a[href$='.pdf']")

        # Filter pdfs of 2023
        pdf_links = [pdf for pdf in pdf_links if '2023' in pdf['href']]

        for link in pdf_links:
            # Name the pdf files using the last portion of each link which are unique in this case
            filename = link['href'].split("/")[-1]
            pdf_content = requests.get(urljoin(base_url,link['href'])).content
            default_storage.save('scraped_pdfs/'+filename, ContentFile(pdf_content))
