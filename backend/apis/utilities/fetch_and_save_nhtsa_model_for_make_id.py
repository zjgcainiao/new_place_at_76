# API utility function. modified in Dec 2023.
from concurrent.futures import thread
from homepageapp.models import NhtsaModel
from .base import models, now, timedelta, logging, NHTSA_API_URL, config, \
        UndefinedValueError, VinNhtsaApiSnapshots, \
        clean_string_in_dictionary_object, aiohttp, NhtsaVariableList, \
        logger
from django.shortcuts import get_object_or_404
from homepageapp.models import NhtsaMake
from .database_sync_to_async import database_sync_to_async
import json
from apis.api_vendor_urls import  nhtsa_get_models_for_make_id_url

async def fetch_and_save_nhtsa_model_for_make_id(make_id):
    if make_id :
        url =  nhtsa_get_models_for_make_id_url(make_id)
    else:
        raise ValueError('a make_id is required to fetch its models.')
    logger.info(
        f'Initiating an api request to {url}.')
    nhtsa_model_list = []
    created_list = []
    make = await database_sync_to_async(get_object_or_404)(NhtsaMake, make_id=make_id)
    if not make:
        logger.error(
            f"No make found for make_id {make_id}.")
        raise ValueError(
            f"No make found for make_id {make_id}.")
    
    defaults={}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()

        # if no data, return an warning in the log
        if data is None:
            logger.warning(
                f"No data returned for {make_id}. Skipping further processing.")
            return
        # Process and save the data as you do in your management script.
        # Fetch the `count`, `message`, `SearchCriteria`, `Results` from the api result.
        count = data.get("Count", None)
        message = data.get("Message", "").strip() or None
        search_criteria = data.get("SearchCriteria", "").strip() or None

        results = data.get("Results")
        if isinstance(results, list) and results:
            logger.info(
                f"result fetched successful for make {make_id}.")
            
            results = results[0]
            # Check if the first object is a dictionary
            if isinstance(results, dict):
                results=results
            else:
                logger.warning(f'the results is not a dictionary for  make {make_id}.')
                results=json.dumps(results)
            if results:
                logger.info(
                    f"result fetched successful for Make {make_id}.")

            # updated_records = await decrement_version_for_vin_async(vin)

            for item in results:
                item = clean_string_in_dictionary_object(item)
                # model_id = item.get("Model_ID")
                model_name = item.get("Model_Name")
                model_id = item.get("Model_ID")
                defaults = {
                    'model_name': model_name,
                    'model_id': model_id,
                }
                
                # updated on 2023-12-24: async function, to create or update in VinNhtsaApiSnapshots model.
                nhtsa_model, created = await database_sync_to_async(NhtsaModel.objects.update_or_create)(
                    make=make,
                        defaults=defaults,
                    )
                logger.info(f'nthsa_model is {nhtsa_model}')
                nhtsa_model_list.append(nhtsa_model)
                created_list.append(created)

        logger.info(
            f'Models related has been saved for {make_id}.')

        if created:
            logger.info(f'saving new models? : {created}.')
        else:
            logger.info(' updating models...')
        logger.info('function is completed.')
        # print('function is completed.')
        # return the data, the number of records downgraded, and if new records are created in the VinNhtsaSnapshots
        return nhtsa_model_list, created_list, count, message

    except (aiohttp.ClientError, aiohttp.ClientPayloadError) as e:
        logger.error(
            f"Failed to fetch models for {make_id}. Error: {e}")
        return None, None, None
    except Exception as e:
        logger.error(
            f"Failed to fetch models for {make_id}. Error: {e}")
        return None, None, None
