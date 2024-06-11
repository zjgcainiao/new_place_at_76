
from celery import shared_task
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
from datetime import datetime, timedelta

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import logging

from apis.utilities import database_sync_to_async
logger = logging.getLogger('django.db')


@shared_task
# @database_sync_to_async
def scrape_and_download_pdfs_task():
    base_url = "https://www.federalreserve.gov/data/sloos.htm"
    response = requests.get(base_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract all links from the specified list in the HTML structure
        links = soup.select("ul.list-unstyled > li > a")

        # Generate full URLs for each link
        search_urls = [urljoin(base_url, link['href'])
                       for link in links if 'sloos' in link['href']]

        for search_url in search_urls:
            # Validate URL
            if not search_url.startswith("http"):
                logger.error(f"Invalid URL: {search_url}")
                # break
                continue

            search_response = requests.get(search_url)
            if search_response.status_code == 200:
                search_soup = BeautifulSoup(
                    search_response.content, 'html.parser')

                # Try to dynamically fetch the year and month from the URL
                year_month_match = re.search(
                    r'sloos-(\d{4})(\d{2})\.htm', search_url)

                # If year and month pattern isn't found, fall back to just the year
                if year_month_match:
                    year = year_month_match.group(1)
                    month = year_month_match.group(2)
                else:
                    year_match = re.search(r'sloos-(\d{4})', search_url)
                    if year_match:
                        year = year_match.group(1)
                        month = None  # Or set a default value/behavior for month
                    else:
                        # Handle the case where no year information is found
                        logger.info(f"No year found in URL: {search_url}")
                        continue

                pdf_links = search_soup.select("a[href$='.pdf']")
                # Filter pdfs based on the dynamically fetched year
                pdf_links = [pdf for pdf in pdf_links if year in pdf['href']]

                for link in pdf_links:
                    filename = link['href'].split("/")[-1]
                    pdf_url = urljoin(base_url, link['href'])
                    pdf_content = requests.get(pdf_url).content
                    default_storage.save(
                        f'scraped_pdfs/{filename}', ContentFile(pdf_content))
                    logger.info(f"Downloaded PDF: {filename}")

    else:
        logger.error(f"Failed to fetch base URL: {base_url}")
