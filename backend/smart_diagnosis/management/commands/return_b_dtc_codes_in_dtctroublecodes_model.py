from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import requests
import logging
from smart_diagnosis.models import DtcTroubleCodes
from internal_users.models import InternalUser
import os
import time
import asyncio
import aiohttp
from django.db import transaction

logger = logging.getLogger('management_script')


class Command(BaseCommand):
    help = "Scrapes DTC trouble codes from https://www.obd-codes.com/"

    BASE_URL = "https://www.obd-codes.com/"

    # Get the base name of the current script
    script_name = os.path.basename(__file__)

    async def fetch(self, session, url):
        try:
            async with session.get(url) as response:
                return await response.text()
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None

    async def get_detail(self, url_suffix):
        """ Fetch details from a given trouble code URL """
        async with aiohttp.ClientSession() as session:
            html_content = await self.fetch(session, self.BASE_URL + url_suffix)
        if not html_content:
            return None
        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            h1_text = soup.find('h1').text
            p_text = soup.find('p', class_='tcode').text

            return {
                'trouble_code_group_name': ' '.join(h1_text.split(' ')[1:]),


                'trouble_code_description': p_text,
                'trouble_code': h1_text.split(' ')[0]
            }
        except Exception as e:
            logger.error(f"Error parsing {url_suffix}: {e}")
            return None

    def handle(self, *args, **kwargs):

        start_time = time.time()  # Record the start time
        logger.info(f'starting management_script {self.script_name}...')
        print(f'starting management_script {self.script_name}...')

        response = requests.get(self.BASE_URL + "/body-codes")
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find all <a> tags with href that start with /B0
        a_tags = soup.find_all('a', href=True)
        links = [a['href'] for a in a_tags if a['href'].startswith('/b0')]

        loop = asyncio.get_event_loop()
        tasks = [self.get_detail(link) for link in links]
        details = loop.run_until_complete(asyncio.gather(*tasks))
        with transaction.atomic():  # wrap in a transaction
            for detail in details:
                # debugging
                # print(f'record looks like {detail}')
                if detail:
                    try:
                        trouble_code = detail['trouble_code']
                        group_name = detail['trouble_code_group_name']
                        description = detail['trouble_code_description']
                        # print(f'getting the trouble code :{trouble_code}')
                        code, created = DtcTroubleCodes.objects.update_or_create(
                            dtc_trouble_code=trouble_code,
                            defaults={
                                'dtc_trouble_code_group_name': group_name,
                                'dtc_trouble_code_description': description,
                                'dtc_trouble_code_description': description,
                                'dtc_trouble_code_description': description,
                            }
                        )
                        self.stdout.write(
                            f"Processed {code.trouble_code}..created?:{created}")
                    except Exception as e:
                        logger.error(
                            f"Error processing {detail['trouble_code']}: {e}")

        self.stdout.write(self.style.SUCCESS(
            f'The {self.script_name} Script run successfully.'))

        # Compute the elapsed time
        elapsed_time = time.time() - start_time
        logger.info(
            f"Script {self.script_name} completed. Total running time: {elapsed_time:.2f} seconds.")
        print(
            f"Script {self.script_name} completed. Total running time: {elapsed_time:.2f} seconds.")
