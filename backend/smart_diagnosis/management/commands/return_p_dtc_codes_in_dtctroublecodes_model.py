import re
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
# import httpx
from asgiref.sync import sync_to_async
logger = logging.getLogger('management_script')


class Command(BaseCommand):
    help = "Scrapes DTC trouble codes from https://www.obd-codes.com/"

    BEGINNING_URL = "https://www.obd-codes.com/trouble_codes/"
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

    def update_or_create_dtc_trouble_codes(self, detail):
        if not detail:
            logger.info("Warning: Received empty or None detail. Skipping update/create.")
            return

        logger.info(
            f'Adding the following record in the DtcTroubleCodes model, DTC code: {detail.get("code")}, description: {detail.get("description")}')
        with transaction.atomic():
            meaning = detail.get('meaning_html', '')
            if len(meaning) > 4000:
                logger.info(
                    f"code_meaning too long ({len(meaning)} characters): {meaning}.")
            defaults = {
                'dtc_trouble_code_group_name': detail.get('group_name'),
                'dtc_trouble_code_description': detail.get('description'),
                'dtc_trouble_code_serverity_html': detail.get('serverity_html', ''),
                'dtc_trouble_code_meaning_html': meaning,
                'dtc_trouble_code_potential_symptoms_html': detail.get('potential_symptoms_html', ''),
                'dtc_trouble_code_potential_causes_html': detail.get('potential_causes_html', ''),
                'dtc_trouble_code_troupleshooting_steps_html': detail.get('troupleshooting_steps_html', ''),
                'dtc_trouble_code_potential_repairs_html': detail.get('potential_repairs_html', ''),
            }
            DtcTroubleCodes.objects.update_or_create(
                dtc_trouble_code=detail.get('code'),
                defaults=defaults
            )
    # second-level url : https://www.obd-codes.com/p00-codes

    async def fetch_second_level(self, session, link):
        group_content = await self.fetch(session, self.BASE_URL + link)
        # logger.info(f'second-level-fetching used group_content is: {group_content}')
        group_soup = BeautifulSoup(group_content, 'html.parser')
        # logger.info(f'fetched group_soup at second level {group_soup}')
        h2_tag = group_soup.find('h2')
        if h2_tag:
            group_name = h2_tag.text
        else:
            group_name = "Unknown Group"
        logger.info(f'fetching group_name {group_name} at url {link}...')
        details_list = []
        for li in group_soup.find_all('li'):
            a_tag = li.find('a')
            details = None
            if a_tag and 'ISO/SAE Reserved'.lower() in a_tag.text.lower():
                # Handle special case where "ISO/SAE Reserved" is present in the anchor tag
                # Extract trouble codes using regular expression
                reserved_codes = re.findall(r'P\d{4}', a_tag.text)
                for code in reserved_codes:
                    details_list.append({
                        'code': code,
                        'description': 'ISO/SAE Reserved',
                        'group_name': group_name
                    })
            elif a_tag:
                # Check and standardize href to the desired format
                revised_link = a_tag['href']

                # Handle case like "p2151" without the slash
                if re.match(r'^p[\da-zA-Z]{4}$', revised_link, re.I):
                    revised_link = '/' + revised_link

                # Handle typo case like "pp657"
                elif re.match(r'^pp[\da-zA-Z]{3}$', revised_link, re.I):
                    revised_link = '/p0' + revised_link[2:]

                # Handle case like "/2134"
                elif re.match(r'^/[\da-zA-Z]{4}$', revised_link, re.I):
                    revised_link = '/p' + revised_link[1:]

                # Check if the revised link is in the correct format before making the request
                if re.match(r'^/p[\da-zA-Z]{4}$', revised_link, re.I):
                    details = await self.get_detail(session, revised_link, group_name)
                else:
                    logger.info(f"Skipped unexpected 'href' format: {revised_link}.")
                    continue
            else:
                code, *description_parts = li.text.split(' ')
                description = ' '.join(description_parts)
                details = {
                    'code': code,
                    'description': description,
                    'group_name': group_name,
                }
            details_list.append(details)

        return details_list
        # third-level data fetching
        # lis = group_soup.find_all('li')
        # for li in lis:
        #     a_tag = li.find('a')
        #     if a_tag:
        #         details_url = self.BASE_URL + a_tag['href']
        #         details_content = await self.fetch(session, details_url)
        #         details_soup = BeautifulSoup(details_content, 'html.parser')

        #         h1_text = details_soup.find('h1').text
        #         code, *description_parts = h1_text.split(' ')
        #         description = ' '.join(description_parts)

        #         h2s = details_soup.find_all('h2')
        #         meanings, symptoms, severities, repairs, causes, troubleshooting = None, None, None, None, None, None

        #         for i in range(len(h2s)):
        #             text = h2s[i].text.lower()
        #             content = h2s[i].find_next_sibling()
        #             while content and content.name != 'h2':
        #                 if "mean" in text:
        #                     meanings = (meanings or "") + str(content)
        #                 elif any(x in text for x in ["symptom", "potential symptom", "possible symptom"]):
        #                     symptoms = (symptoms or "") + str(content)
        #                 elif "severity" in text:
        #                     severities = (severities or "") + str(content)
        #                 elif any(x in text for x in ["repair", "potential repair"]):
        #                     repairs = (repairs or "") + str(content)
        #                 elif any(x in text for x in ["cause", "potential cause"]):
        #                     causes = (causes or "") + str(content)
        #                 elif "troubleshooting" in text:
        #                     troubleshooting = (
        #                         troubleshooting or "") + str(content)
        #                 content = content.find_next_sibling()

        #         details = {
        #             'code': code,
        #             'group_name': group_name,
        #             'description': description,
        #             'meaning': meanings,
        #             'symptoms': symptoms,
        #             'severity': severities,
        #             'repairs': repairs,
        #             'causes': causes,
        #             'troubleshooting': troubleshooting
        #         }

        #     else:
        #         code, *description_parts = li.text.split(' ')
        #         description = ' '.join(description_parts)
        #         details = {
        #             'code': code,
        #             'group_name': group_name,
        #             'description': description,
        #         }

        #     details_list.append(details)
        # return details_list

    async def get_detail(self, session, url_suffix, group_name):
        """ Fetch details from a given trouble code URL """
        # Check and skip if url_suffix doesn't match the expected pattern
        if not re.match(r'^/p[\da-zA-Z]{4}$', url_suffix, re.I):
            logger.info(f"Skipping unexpected URL suffix: {url_suffix}.")
            return None

        html_content = await self.fetch(session, self.BASE_URL + url_suffix)
        if not html_content:
            return None
        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            code = url_suffix.split('/')[-1]
            code = code.upper()

            h1_text = soup.find('h1').text
            code_incorrect, *description_parts = h1_text.split(' ')
            description = ' '.join(description_parts)

            if not re.match(r'^p[\da-zA-Z]{4}$', code_incorrect, re.I):
                # re.I makes the match case insensitive, so it matches P or p
                logger.info(
                    f"Unexpected trouble code: {code_incorrect} from h1 text for url: {url_suffix}. correct code: {code}.")
            details = {
                'code': code,
                'description': description,
                'group_name': group_name,  # Add this line
            }

            # Mapping of h2 keywords to the detail keys
            h2_keywords_map = {
                ('means', 'meaning', 'that mean'): 'meaning_html',
                ('symptoms', 'potential symptoms', 'possible symptoms'): 'potential_symptoms_html',
                ('severity',): 'serverity_html',
                ('potential repairs', 'repairs'): 'potential_repairs_html',
                ('causes', 'potential causes', 'common causes', 'possible causes'): 'potential_causes_html',
                ('troubleshooting',): 'troupleshooting_steps_html',
            }

            h2s = soup.find_all('h2')
            for h2 in h2s:
                h2_text = h2.text.lower()
                if h2_text:
                    h2_text = h2_text.strip()

                # Find which key this h2 corresponds to
                for keywords, detail_key in h2_keywords_map.items():
                    if any(keyword in h2_text for keyword in keywords):
                        # Get all sibling tags until the next h2
                        content_parts = []
                        for sibling in h2.find_next_siblings():
                            if sibling.name == 'h2':
                                break
                            content_parts.append(str(sibling))

                        details[detail_key] = ''.join(content_parts)
                        break

            return details

        except Exception as e:
            logger.error(f"Error parsing {url_suffix}: {e}")
            return None

    async def handle_async(self, *args, **kwargs):

        start_time = time.time()  # Record the start time
        logger.info(f'starting management_script {self.script_name}...')

        async with aiohttp.ClientSession() as session:
            logger.info(
                f'the beginning url to use looks like: {self.BEGINNING_URL}.')
            html_content = await self.fetch(session, self.BEGINNING_URL)
            soup = BeautifulSoup(html_content, 'html.parser')

            # getting from the P27--codes the 100 bundle
            divs = soup.find_all('div', class_=["span_1_of_2"])
            first_level_links = [a['href']
                                 for div in divs for a in div.find_all('a', href=True)]
            logger.info(
                f'total number of first-level-url links: {len(first_level_links)}')
            for link in first_level_links:
                logger.info(f'first-level-url-link {link}.')
            # Now we initiate the second-level fetch tasks
            second_level_tasks = [self.fetch_second_level(
                session, link) for link in first_level_links]
            details_list_of_lists = await asyncio.gather(*second_level_tasks)

            # Flatten the list of lists
            details_list = [
                item for sublist in details_list_of_lists for item in sublist]

            for detail in details_list:
                await sync_to_async(self.update_or_create_dtc_trouble_codes, thread_sensitive=True)(detail)

        self.stdout.write(self.style.SUCCESS(
            f'The {self.script_name} Script run successfully.'))

        # Compute the elapsed time
        elapsed_time = time.time() - start_time
        logger.info(
            f"Script {self.script_name} completed. Total running time: {elapsed_time:.2f} seconds.")


    def handle(self, *args, **kwargs):
        asyncio.run(self.handle_async(*args, **kwargs))
