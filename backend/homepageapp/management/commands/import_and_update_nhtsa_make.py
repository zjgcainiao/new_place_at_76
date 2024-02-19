# Assuming you have a model named NhtsaMake
from homepageapp.models import NhtsaMake
from apis.utilities import  database_sync_to_async
from asgiref.sync import sync_to_async
# from apis.utilities import  fetch_from_api_url
from apis.api_vendor_urls import NHTSA_GET_ALL_MAKES_URL
from .base import logger,clean_string_in_dictionary_object, time,os,BaseCommand, transaction
from aiohttp import ClientSession
import asyncio

class Command(BaseCommand):
    help = 'Import data from the API URL into the NhtsaMake model'
    # Get the base name of the current script
    script_name = os.path.basename(__file__)

    
    def create_or_update_nhtsa_make(self,make_id, make_name):
        with transaction.atomic():
            return NhtsaMake.objects.update_or_create(
                make_id=make_id,
                defaults={'make_name': make_name}
            )

    async def handle_async(self, *args, **options):

        start_time = time.time()  # Record the start time
        logger.info(f'starting management script {self.script_name}...')

        url = NHTSA_GET_ALL_MAKES_URL
        if not url:
            raise ValueError('API URL is not defined')

        # Fetch data from the API URL
        logger.info(f'Fetching makes from the API URL: {url}')
        async with ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    nhtsa_data = await response.json()
                    if nhtsa_data:
                        results = nhtsa_data.get('Results', [])
                        # results = clean_string_in_dictionary_object(results)
                        for result in results:
                            make_id = result.get('Make_ID')
                            make_name = result.get('Make_Name')
                            if make_id and make_name:
                                await  database_sync_to_async(self.create_or_update_nhtsa_make)(make_id, make_name)

                    else:
                        logger.error('Failed to fetch data from the API URL')
                        return {
                                'error': f'Failed to fetch data from the api url: {url}.',
                                'status': response.status
                            }
                else:
                    return {
                        'error': f'Failed to fetch data from the api url: {url}.',
                        'status': response.status
                    }

        logger.info(f'fetching successful...next step is to import the data to NhtsaMakes....')


        end_time = time.time()
        elapsed_time = end_time - start_time
        logger.info(f"Script {self.script_name} completed. Total running time: {elapsed_time:.2f} seconds.")

    def handle(self, *args, **kwargs):
        asyncio.run(self.handle_async(*args, **kwargs))
