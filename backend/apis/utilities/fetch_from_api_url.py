import asyncio
import aiohttp
from rest_framework.response import Response
from rest_framework.decorators import api_view
from apis.utilities import database_sync_to_async
from aiohttp import ClientSession
from .base import logger


# 
async def fetch_from_api_url(url):
    async with ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                external_data = await response.json()
                logger.info(f'Fetching data from the api url: {url} successful...')
                return external_data
            else:
                return {
                    'error': f'Failed to fetch data from the api url: {url}.',
                    'status': response.status
                }
            
