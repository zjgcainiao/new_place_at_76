from .base import logger


# the function compares the field mapping between the API results (such as nthsa api) and its corresponding Django model
def validate_field_mappings(results, model_cls, field_mappings):

    if isinstance(results, list):
        results = results[0] if results else {}

    # 1. Verify against API results
    results_fields = results.keys() if isinstance(results, dict) else []
    for api_field, model_field in field_mappings.items():
        if api_field not in results_fields:
            logger.warning(f"Field '{api_field}' is missing in the API results.")
        # if model_field not in results_fields:
        #     logger.warning(f"Field '{model_field}' is missing in the API results.")

    # 2. Verify against Django model
    model_fields = [field.name for field in model_cls._meta.get_fields()]
    for api_field, model_field in field_mappings.items():
        if model_field not in model_fields:
            logger.warning(f"Field '{model_field}' is missing in the Django model.")

    logger.info("Field mapping verification completed.")

