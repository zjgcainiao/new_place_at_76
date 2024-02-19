import requests
from bs4 import BeautifulSoup
from datetime import datetime
from django.core.files import File
from shops.models import EconomicReport
import logging 
from django.db import transaction
from urllib.parse import urljoin
from django.core.files.base import ContentFile

logger = logging.getLogger('django.db')



# Function to find the specific section
def find_specific_section(soup, section_title=lambda text: "Reports to" in text):# string=lambda text: "Reports to" in text
    headers = soup.find_all('h4', string=section_title)
    for header in headers:
        next_sibling = header.find_next_sibling("ul")
        if next_sibling:
            return next_sibling
    return None

# Function to process and download reports
def process_and_download_reports(section,base_url="https://www.federalreserve.gov/"):
    reports = []
    for li in section.find_all('li'):
        try:
            a = li.find('a')
            link = a['href']
            full_link = urljoin(base_url, link) # full link
            title = a.text.strip()
            date_str = li.text.split('(')[-1].split(')')[0]
            publication_date = datetime.strptime(date_str, "%B %d, %Y").date()

            # Prepare report data
            reports.append({
                "name": 'BFTP_Report' + title ,#title,
                "publication_date": publication_date,
                "source_url": full_link,
                'link': link,
            })
        except Exception as e:
            print(f"An error occurred while processing {li}: {e}")
    return reports

# fetch BFTP reports. Main function
def fetch_economic_reports():
    # Example URL where the reports are located
    url = "https://www.federalreserve.gov/financial-stability/bank-term-funding-program.htm"
    base_url = "https://www.federalreserve.gov/"

    # Send a GET request to the URL
    response = requests.get(url)
    response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX/5XX

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    # Process the specific section
    specific_section = find_specific_section(soup)
    if specific_section:
        reports_to_download = process_and_download_reports(specific_section, base_url)
        logger.info(f"Found {len(reports_to_download)} reports to download.")

        # Atomic database transaction
        with transaction.atomic():
            for report in reports_to_download:
                # Check if the report already exists to avoid duplicates
                obj, created = EconomicReport.objects.update_or_create(
                    name=report["name"],
                    publication_date=report["publication_date"],
                    source_url= report['source_url'],
                    defaults={
                        # "source_url": report["source_url"],
                        "frequency": "one-time",

                    }  # Use defaults to update fields if the object is not created but found
                )

                if created or not obj.saved_copy:  # If the report is newly created or doesn't have a saved copy yet
                    # Download the PDF
                    pdf_response = requests.get(report["source_url"])
                    pdf_response.raise_for_status()

                    # Assuming the name of the PDF file is extracted from the URL
                    file_name = report["link"].split('/')[-1]

                    # Instead of saving the file to a path, create a ContentFile for Django's FileField
                    obj.saved_copy.save(file_name, ContentFile(pdf_response.content), save=True)
                    logger.info(f"Downloaded and saved: {report['name']}")
                    # obj.save()
                else:
                    logger.error(f"Report already exists and has a saved copy: {report['name']}")
                    input("Report already exists and has a saved copy. Press Enter to continue...")
    else:
        logger.error("Specific section not found.")
    