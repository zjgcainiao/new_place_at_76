from .base import logger, fake, datetime, transaction, models, re, Paginator

def update_model_with_dummy_data(model, databaseName='demo', chunk_size=1000):
    logger.info(f"Updating the model {model} in database {databaseName}...")
    updated_records_count = 0  # Counter for updated records
    # reference to the fake methods but not calling them yet.
    patterns_to_update = {
        r"(_first_name|first_name|FirstName)": fake.first_name,
        r"(_last_name|last_name|LastName)": fake.last_name,
        r"(_middle_name|middle_name|MiddleName)": lambda: "Middle " + datetime.now().strftime('%y%m%d'),
        r"(PhoneNum|phone_number$|Phone$|phone$)": lambda: fake.phone_number().split('x')[0].strip(),
        r"(address_line_01|^address_|Address$)": fake.street_address,
        r"(Email$|email$|^email_address)": fake.email,
        r"(address_city|city)": fake.city,
        r"(zip_code|zipcode)": fake.postcode,
        r"(VIN|vin)": fake.vin,
        r"(License|licence_plate_number|license_plate_nbr)": fake.license_plate,
    }

    # Paginate the queryset
    objects_paginator = Paginator(
        model.objects.using(databaseName).all(), chunk_size)

    for page_num in objects_paginator.page_range:

        with transaction.atomic(databaseName):
            # model.objects.all():
            for obj in objects_paginator.page(page_num).object_list:
                updated = False  # Initialize the updated flag
                for field in obj._meta.fields:

                    for pattern, fake_data_func in patterns_to_update.items():
                        if re.search(pattern, field.name):
                            # Check if it's a CharField or EmailField before updating
                            if isinstance(field, models.CharField) or isinstance(field, models.EmailField):
                                setattr(obj, field.name, fake_data_func())
                                updated = True
                            else:
                                logger.info(
                                    f" {field.name} in {model} is not a CharField. Skipping..")
                                continue

                if updated:
                    obj.save(using=databaseName)
                    updated_records_count += 1
                    # logger.info(
                    #     f"Updated record with ID: {obj.pk} in model {model.__name__}.")

    return updated_records_count