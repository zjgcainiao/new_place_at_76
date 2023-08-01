import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

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
        
        # Find all pdf links
        pdf_links = soup.select("a[href$='.pdf']")

        # Filter pdfs of 2023
        pdf_links = [pdf for pdf in pdf_links if '2023' in pdf['href']]

        for link in pdf_links:
            # Name the pdf files using the last portion of each link which are unique in this case
            filename = os.path.join("pdfs", link['href'].split("/")[-1])
            # Download the pdfs to the specified location
            with open(filename, 'wb') as f:
                f.write(requests.get(urljoin(base_url, link['href'])).content)
