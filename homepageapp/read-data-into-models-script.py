# updated on 2023-09-17
# this script intends to write data from json files into existing data tables. update or create.

import csv
import json
import os
from decimal import Decimal, ROUND_HALF_UP
from homepageapp.models import EmailsNewSQL02Model as Email, CustomersNewSQL02Model as Customer
from homepageapp.models import AddressesNewSQL02Model as Address, PhonesNewSQL02Model as Phone, VehiclesNewSQL02Model as Vehicle
from homepageapp.models import CustomerAddressesNewSQL02Model as CustomerAddress, CustomerEmailsNewSQL02Model as CustomerEmails
from homepageapp.models import CustomerPhonesNewSQL02Model as CustomerPhones, PhonesNewSQL02Model as Phones
from homepageapp.models import EmailsNewSQL02Model as Emails, TaxesModel as Taxes
from homepageapp.models import PhoneDescModel as PhoneDesc, CategoryModel as Category, TextMessagesModel as TextMessage
from homepageapp.models import AccountClassModel as AccountClass, InvoiceStatusModel as InvoiceStatus

from homepageapp.models import MakesNewSQL02Model as Make, ModelsNewSQL02Model as Model, BrakesModel as Brake, BodyStylesModel as BodyStyle
from homepageapp.models import EnginesModel as Engine, TransmissionsModel as Transmission, GVWsModel as GVW, DrivesModel as Drive, SubmodelsModel as SubModel
from homepageapp.models import MyShopVehicleConfigsModel as MyShopVehicleConfig, VehicleConfigMyShopConfigsModel as VehicleConfigMyShopConfig
from homepageapp.models import TextMessagesModel as TextMessage

from homepageapp.models import RepairOrderPhasesNewSQL02Model as RepairOrderPhase, RepairOrdersNewSQL02Model as RepairOrder
from homepageapp.models import RepairOrderLineItemSquencesNewSQL02Model as RepairOrderLineItem
from homepageapp.models import CannedJobsNewSQL02Model as CannedJob, LineItemsNewSQL02Model as LineItem
from homepageapp.models import PartItemModel as PartItem, PartsModel as Part, LaborItemModel as LaborItem
from homepageapp.models import lineItemTaxesNewSQL02Model as LineItemTax, NoteItemsNewSQL02Model as NoteItem
from homepageapp.models import AccountClassModel as AccountClass, PaymentsModel as Payment, PaymentTransactionsModel as PaymentTransaction
from homepageapp.models import VehicleNotesModel as VehicleNotes
from homepageapp.models import Vendors, VendorAdddresses, VendorLinks, VendorTypes, 
from talent_management.models import TalentsModel as Talent

import pandas as pd
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.utils import timezone
import logging
from django.db import transaction
from core_operations.common_functions import clean_string_in_dictionary_object

# Initialize logging 2023-09-17
logging.basicConfig(filename='data_import_v01.log', level=logging.ERROR)

module_dir = '/Users/stephenwang/Documents/myiCloudCopy-76ProLubePlus/13-Information-Technology/003-IT_New-Site-Development-2022/New_site_database-data-migration-python-scripts/old_db_jsons'
suffix_pattern = '_20230115.json'


def parse_time(datetime_string):
    if not datetime_string:
        # If time_str is None or empty, return None
        return None
    try:
        formatted_datetime = datetime.strptime(
            datetime_string, '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        formatted_datetime = datetime.strptime(
            datetime_string, '%Y-%m-%dT%H:%M:%S.%f')
    return formatted_datetime

# customized uitity function get_or_none.
# added on 2023-09-17 to simplify the data writing code


def get_or_none(model, pk):
    try:
        return model.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return None


def make_timezone_aware(input_datetime, datetime_formats=['%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%dT%H:%M:%S.%f']):
    """
    Convert a naive datetime string or datetime object to a timezone-aware datetime object.

    Parameters:
    - input_datetime: The naive datetime string or datetime object.
    - datetime_formats: A list of datetime formats to try for parsing. Defaults to include common formats.

    Returns:
    - A timezone-aware datetime object or None.
    """
    if input_datetime is None:
        return None

    if isinstance(input_datetime, datetime):
        native_datetime = input_datetime
    elif isinstance(input_datetime, str):
        native_datetime = None
        for fmt in datetime_formats:
            try:
                native_datetime = datetime.strptime(input_datetime, fmt)
                break
            except ValueError:
                continue
        if native_datetime is None:
            return None
    else:
        raise TypeError(
            "The input must be either a datetime object or a string.")

    return timezone.make_aware(native_datetime)


# Load all foreign key objects into a dictionary for quick lookup. RepairOrderPhase, Customer and Vehicle models.
# pre-load phases, customers, vehicles, phones and emails and etc
phase_dict = {
    phase_obj.repair_order_phase_id: phase_obj for phase_obj in RepairOrderPhase.objects.all()}

repairorder_dict = {
    repairorder_obj.repair_order_id: repairorder_obj for repairorder_obj in RepairOrder.objects.all()}
phone_dict = {phone.phone_id: phone for phone in Phones.objects.all()}
email_dict = {email.email_id: email for email in Emails.objects.all()}
taxes_dict = {tax.tax_id: tax for tax in Taxes.objects.all()}
phonedesc_dict = {
    phonedesc.phone_desc_id: phonedesc for phonedesc in PhoneDesc.objects.all()}
lineitem_dict = {
    lineitem.line_item_id: lineitem for lineitem in LineItem.objects.all()}
model_dict = {model.model_id: model for model in Model.objects.all()}
make_dict = {make.make_id: make for make in Make.objects.all()}
engine_dict = {engine.engine_id: engine for engine in Engine.objects.all()}
submodel_dict = {
    submodel.submodel_id: submodel for submodel in SubModel.objects.all()}
bodystyle_dict = {
    bodystyle.body_style_id: bodystyle for bodystyle in BodyStyle.objects.all()}
drive_dict = {drive.drive_id: drive for drive in Drive.objects.all()}
gvw_dict = {gvw.gvw_id: gvw for gvw in GVW.objects.all()}
transmission_dict = {
    trans.transmission_id: trans for trans in Transmission.objects.all()}
brake_dict = {brake.brake_id: brake for brake in Brake.objects.all()}

myshopvehicleconfig_dict = {myshopvehicleconfig.myshop_vehicle_config_id:
                            myshopvehicleconfig for myshopvehicleconfig in MyShopVehicleConfig.objects.all()}

customer_dict = {
    customer_obj.customer_id: customer_obj for customer_obj in Customer.objects.all()}
vehicle_dict = {
    vehicle_obj.vehicle_id: vehicle_obj for vehicle_obj in Vehicle.objects.all()}

# repairorder into repairorders_new_03 sql Table


# def testing(request):
# Addresses into Addressess_new_03 sql Table
model_name = 'Addresses'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    data = json.load(f)
    for aa in data:
        aa_instance = Address(
            address_id=aa['AddressId'],
            address_type_id=aa['AddressTypeId'],
            address_company_or_ATTN=aa['Company'],
            address_line_01=aa['Address'],
            address_city=aa['City'],
            address_state=aa['State'],
            address_zip_code=aa['ZipCode'],
            address_last_updated_at=aa['LastChangeDate'],
        )
        aa_instance.save()

# customer into customers_new_03 sql table
model_name = 'Customer'
file_path = os.path.join(module_dir, (model_name + suffix_pattern))
with open(file_path, 'r') as f:
    customer_data = json.load(f)
    with transaction.atomic():  # wrap in a transaction
        for aa in customer_data:
            # the newer way to update or create data in CustomersNewSQL02Model
            # confirm expected key exists:
            if 'CustId' not in aa:
                logging.error(f"Skipping entry due to missing 'CustId': {aa}")
                exit

            # Convert naive datetime to timezone-aware datetime.
            # str
            date_str_first = aa.get('FirstVisited', None)
            date_str_last = aa.get('LastVisited', None)

            naive_datetime_first = datetime.strptime(
                date_str_first, '%Y-%m-%dT%H:%M:%S') if date_str_first else None
            naive_datetime_last = datetime.strptime(
                date_str_last, '%Y-%m-%dT%H:%M:%S') if date_str_last else None

            # Convert naive datetime to timezone-aware datetime
            first_visit_date = timezone.make_aware(
                naive_datetime_first) if naive_datetime_first else None
            last_visit_date = timezone.make_aware(
                naive_datetime_last) if naive_datetime_last else None
            defaults = {
                'customer_title_id': aa['TitleId'],
                'customer_first_name': aa['FirstName'],
                'customer_last_name': aa['LastName'],
                'customer_dob': aa['DOB'],
                'customer_spouse_name': aa['SpouseName'],
                'customer_is_okay_to_charge': aa['ChargeOK'],
                'customer_memo_1': aa['Remarks'],
                'customer_resale_permit_nbr': aa['ResaleNum'],
                'customer_is_in_social_crm': aa['IncludeInCRMCampaign'],
                'customer_is_tax_exempt': aa['TaxExempt'],
                'customer_last_visit_date': last_visit_date,
                'customer_first_visit_date': first_visit_date,
                'customer_hear_from_us_type': aa['RefTypeId'],
                'customer_is_deleted': aa['IsDeleted'],
                'customer_is_created_from_appointments': aa['IsFromSchedule'],
                'customer_does_allow_SMS': aa['SMSAllowed'],
                'customer_email_address_in_json': aa['EmailAddress'],
                'customer_last_updated_at': aa['LastChangeDate'],
                'customer_fleet_vendor_id': aa['FleetVendorId'],
            }
            try:
                customer_instance, created = Customer.objects.update_or_create(
                    customer_id=aa['CustId'],
                    defaults=defaults
                )
                customer_instance.full_clean()
                customer_instance.save()
            except ValidationError as e:
                logging.error(
                    f"Validation error for Customer ID {aa['CustId']}: {e}")
                print(f"Validation error for Customer ID {aa['CustId']}: {e}")
            except Exception as e:
                logging.error(
                    f"An error occurred while updating/creating Customer with ID {aa['CustId']}: {e}")
                print(
                    f"An error occurred while updating/creating Customer with ID {aa['CustId']}: {e}")

            # aa_instance = Customer(
            #     customer_id=aa['CustId'],
            #     customer_title_id=aa['TitleId'],
            #     customer_first_name=aa['FirstName'],
            #     customer_last_name=aa['LastName'],
            #     customer_dob=aa['DOB'],
            #     customer_spouse_name=aa['SpouseName'],
            #     customer_is_okay_to_charge=aa['ChargeOK'],
            #     customer_memo_1=aa['Remarks'],
            #     customer_resale_permit_nbr=aa['ResaleNum'],
            #     customer_is_in_social_crm=aa['IncludeInCRMCampaign'],
            #     customer_is_tax_exempt=aa['TaxExempt'],
            #     customer_last_visit_date=aa['LastVisited'],
            #     customer_first_visit_date=aa['FirstVisited'],
            #     customer_hear_from_us_type=aa['RefTypeId'],
            #     customer_is_deleted=aa['IsDeleted'],
            #     customer_is_created_from_appointments=aa['IsFromSchedule'],
            #     customer_does_allow_SMS=aa['SMSAllowed'],
            #     customer_email_address_in_json=aa['EmailAddress'],
            #     customer_last_updated_at=aa['LastChangeDate'],
            #     customer_fleet_vendor_id=aa['FleetVendorId'],
            #     # customer_memo_1 = '' # empty string for the field.
            # )
            # aa_instance.save()

# Email to emails_new_03 sql table
file_path = os.path.join(module_dir, 'Email'+suffix_pattern)
with open(file_path, 'r') as f:
    email_data = json.load(f)
    for aa in email_data:
        aa_instance = Email(
            email_id=aa['Id'],
            email_type_id=aa['EmailTypeId'],
            email_address=aa['Email'],
            email_description=aa['Description'],
            email_last_updated_at=aa['LastChangeDate']
        )
        aa_instance.save()

# phonedesc model into phonedescs_new_03 sql table
model_name = 'PhoneDesc'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    data = json.load(f)
    for aa in data:
        aa_instance = PhoneDesc(
            phone_desc_id=aa['PhoneDescId'],
            phone_desc=aa['Description'],
            phone_order=aa['PhoneOrder'],
            phone_desc_default_type=aa['DefaultType'],
            phone_desc_last_updated_at=aa['LastChangeDate'],
        )
        aa_instance.save()

model_name = 'Category'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    # when the file becomes big, break down into 1000 records per piece
    # added on 2023-04-10
    # while True:
    #     chunk = f.read(1000)
    #     if not chunk:
    #         break
    data_list = []
    data = json.load(f)
    for aa in data:
        aa_instance = Category(
            category_id=aa['CategoryId'],
            category_description=aa['Description'],
            category_display=aa['Display'],
            category_last_updated_at=aa['LastChangeDate'],
        )
        aa_instance.save()

# phone model into phones_new_03 sql table
file_path = os.path.join(module_dir, 'PhoneNum' + suffix_pattern)
with open(file_path, 'r') as f:
    data = json.load(f)
    for aa in data:
        phone_desc_id = aa['PhoneDescId']
        if phone_desc_id is not None:
            try:
                phone_desc_obj = phonedesc_dict.get(phone_desc_id)
            except ObjectDoesNotExist:
                phone_desc_obj = None
        else:
            phone_desc_obj = None

        aa_instance = Phone(
            phone_id=aa['PhoneId'],
            phone_desc_id=phone_desc_obj,
            phone_number=aa['PhoneNum'],
            phone_number_ext=aa['Ext'],
            phone_displayed_name=aa['Display'],
            phone_memo_01=aa['Note'],
            phone_last_updated_at=aa['LastChangeDate'],
        )
        aa_instance.save()

# customerphone model into customerphones_new_03 sql table
model_name = 'CustomerPhones'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    data = json.load(f)
    for aa in data:
        aa_instance = CustomerPhones(
            phone_id=aa['PhoneId'],
            customer_id=aa['CustId'],
            customerphone_last_updated_at=aa['LastChangeDate'],
        )
        aa_instance.save()

# import intial data into customeremails_new_03 sql table for 'customeremail' model
model_name = 'CustomerEmail'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    data = json.load(f)
    for aa in data:
        aa_instance = CustomerEmails(
            customeremail_id=aa['Id'],
            customer_id=aa['CustId'],
            email_id=aa['EmailId'],
            customeremail_is_selected=aa['IsSelected'],
            customeremail_last_updated_at=aa['LastChangeDate'],
        )
        aa_instance.save()

# CustomerAddresses into CustomerAddressess_new_03 sql Table
model_name = 'CustomerAddresses'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    data = json.load(f)
    for aa in data:
        aa_instance = CustomerAddress(
            address_id=aa['AddressId'],
            customer_id=aa['CustID'],
            customeraddress_last_updated_at=aa['LastChangeDate'],

        )
        aa_instance.save()


# Engine model into engines_new_03 sql table
model_name = 'Engine'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    data = json.load(f)
    for aa in data:
        aa_instance = Engine(
            engine_id=aa['EngineId'],
            engine_displacement_CID=aa['DisplacementCID'],
            engine_displacement_liter=aa['DisplacementLiters'],
            engine_number_of_cylinder=aa['NumberOfCylinders'],
            engine_valve_per_cyclinder=aa['ValvesPerCylinder'],
            engine_head_configuration_type=aa['HeadConfigurationType'],
            engine_boost_type=aa['BoostType'],
            engine_ignition_system=aa['IgnitionSystem'],
            engine_vin_code=aa['VinCode'],
            engine_fuel_system=aa['FuelSystem'],
            engine_fuel_delivery_method_type=aa['FuelDeliveryMethodType'],
            engine_fuel_type=aa['FuelType'],
            engine_fuel_control_type=aa['FuelControlType'],
            engine_block_configuration=aa['BlockConfiguration'],
            engine_fuel_system_configuration=aa['FuelSystemConfiguration'],
        )
        aa_instance.save()

# transmission model into transmission_new_03 sql table
model_name = 'Transmission'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    data = json.load(f)
    for aa in data:
        aa_instance = Transmission(
            transmission_id=aa['TransmissionId'],
            transmission_type=aa['TransmissionType'],
            tranmission_manufacturer_code=aa['ManufacturerCode'],
            transmission_control_type=aa['ControlType'],
            tranmission_is_electronic_controlled=aa['ElectronicControlled'],
            transmission_number_of_speed=aa['NumberOfSpeeds'],
        )
        aa_instance.save()

# GWV model into gvws_new_03 sql table
model_name = 'GVW'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    data = json.load(f)
    for aa in data:
        aa_instance = GVW(
            gvw_id=aa['GVWId'],
            gvw_text=aa['GVWText'],
        )
        aa_instance.save()

# brake model into brakes_new_03 sql table
model_name = 'Brake'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    data = json.load(f)
    for aa in data:
        aa_instance = Brake(
            brake_id=aa['BrakeId'],
            brake_system_type=aa['BrakeSystemType'],
        )
        aa_instance.save()

# drive model into drives_new_03 sql table
model_name = 'Drive'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    data = json.load(f)
    for aa in data:
        aa_instance = Drive(
            drive_id=aa['DriveId'],
            drive_type=aa['DriveType'],
        )
        aa_instance.save()


# submodel model into submodel_new_03 sql table
model_name = 'SubModel'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    data = json.load(f)
    for aa in data:
        submodel_model_id = aa['ModelId']
        if submodel_model_id is not None:
            try:
                submodel_model_obj = model_dict.get(submodel_model_id)
            except ObjectDoesNotExist:
                submodel_model_obj = None
        else:
            submodel_model_obj = None

        aa_instance = SubModel(
            submodel_id=aa['SubModelId'],
            submodel_model=submodel_model_obj,
            submodel_name=aa['Name'],
            submodel_DMV_id=aa['DMVId'],
        )
        aa_instance.save()

# bodystyle model into bodystyles_new_03 sql table
model_name = 'BodyStyle'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    data = json.load(f)
    for aa in data:
        aa_instance = BodyStyle(
            body_style_id=aa['BodyStyleId'],
            body_style_name=aa['Name'].strip(),
        )
        aa_instance.save()


# myshopvehicleconfig model into myshopvehicleconfigs_new_03 sql table
model_name = 'ShopMgtVehicleConfig'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    data = json.load(f)
    for aa in data:
        myshop_make_id = aa['MakeId']
        if myshop_make_id is not None:
            try:
                myshop_make_obj = make_dict.get(myshop_make_id)
            except ObjectDoesNotExist:
                myshop_make_obj = None
        else:
            myshop_make_obj = None

        myshop_model_id = aa['ModelId']
        if myshop_model_id is not None:
            try:
                myshop_model_obj = model_dict.get(myshop_model_id)
            except ObjectDoesNotExist:
                myshop_model_obj = None
        else:
            myshop_model_obj = None

        myshop_submodel_id = aa['SubModelId']
        if myshop_submodel_id is not None:
            try:
                myshop_submodel_obj = submodel_dict.get(myshop_submodel_id)
            except ObjectDoesNotExist:
                myshop_submodel_obj = None
        else:
            myshop_submodel_obj = None

        myshop_bodystyle_id = aa['BodyStyleId']
        if myshop_bodystyle_id is not None:
            try:
                myshop_bodystyle_obj = bodystyle_dict.get(myshop_bodystyle_id)
            except ObjectDoesNotExist:
                myshop_bodystyle_obj = None
        else:
            myshop_bodystyle_obj = None

        myshop_engine_id = aa['EngineId']
        if myshop_engine_id is not None:
            try:
                myshop_engine_obj = engine_dict.get(myshop_engine_id)
            except ObjectDoesNotExist:
                myshop_engine_obj = None
        else:
            myshop_engine_obj = None

        myshop_brake_id = aa['BrakeId']
        if myshop_brake_id is not None:
            try:
                myshop_brake_obj = brake_dict.get(myshop_brake_id)
            except ObjectDoesNotExist:
                myshop_brake_obj = None
        else:
            myshop_brake_obj = None

        myshop_transmission_id = aa['TransmissionId']
        if myshop_transmission_id is not None:
            try:
                myshop_transmission_obj = transmission_dict.get(
                    myshop_transmission_id)
            except ObjectDoesNotExist:
                myshop_transmission_obj = None
        else:
            myshop_transmission_obj = None

        myshop_GVW_id = aa['GVWId']
        if myshop_GVW_id is not None:
            try:
                myshop_GVW_obj = gvw_dict.get(myshop_GVW_id)
            except ObjectDoesNotExist:
                myshop_GVW_obj = None
        else:
            myshop_GVW_obj = None

        myshop_drive_id = aa['DriveId'],
        if myshop_drive_id is not None:
            try:
                myshop_drive_obj = drive_dict.get(myshop_drive_id)
            except ObjectDoesNotExist:
                myshop_drive_obj = None
        else:
            myshop_drive_obj = None
        # when the MyShopVehicleConfig instance can be found via myshop_vehicle_config_id, rewrite the following fields
        if MyShopVehicleConfig.objects.get(pk=aa['ShopMgtVehicleConfigId']) is not None:
            aa_instance = MyShopVehicleConfig()
            if myshop_make_obj is not None:
                aa_instance.myshop_make = myshop_make_obj
            if myshop_bodystyle_obj is not None:
                aa_instance.myshop_bodystyle = myshop_bodystyle_obj
            if myshop_model_obj is not None:
                aa_instance.myshop_model = myshop_model_obj
            if myshop_submodel_obj is not None:
                aa_instance.myshop_submodel = myshop_submodel_obj
            if myshop_drive_obj is not None:
                aa_instance.myshop_drive = myshop_drive_obj
            if myshop_transmission_obj is not None:
                aa_instance.myshop_transmission = myshop_transmission_obj
            if myshop_brake_obj is not None:
                aa_instance.myshop_brake = myshop_brake_obj
            if myshop_GVW_obj is not None:
                aa_instance.myshop_GVW = myshop_GVW_obj
            if myshop_engine_obj is not None:
                aa_instance.myshop_engine = myshop_engine_obj
        else:
            aa_instance = MyShopVehicleConfig(
                myshop_vehicle_config_id=aa['ShopMgtVehicleConfigId'],
                myshop_year_id=aa['Year'],
                myshop_make_id=myshop_make_id,  # myshop_make_obj,
                myshop_model_id=myshop_model_id,  # myshop_model_obj,
                myshop_submodel_id=myshop_submodel_id,  # myshop_submodel_obj,
                myshop_bodystyle_id=myshop_bodystyle_id,  # myshop_bodystyle_obj,
                myshop_engine_id=myshop_engine_id,  # myshop_engine_obj ,
                myshop_brake_id=myshop_brake_id,  # myshop_brake_obj,
                myshop_transmission=myshop_transmission_obj,  # myshop_transmission_id,
                myshop_GVW=myshop_GVW_obj,  # myshop_GVW_id,
                myshop_drives=myshop_drive_obj,  # myshop_drive_id,
            )
        aa_instance.save()


# VehicleConfigMyshopConfig model into vehicleconfigmyshopconfig_new_03 sql table

# encounter an problem that myshop_vehicle_config_id becomes NULL
model_name = 'VehicleConfigurationMapping'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    data = json.load(f)
    for aa in data:
        myshop_vehicle_config_id = aa['ShopMgtVehicleConfigId']
        if myshop_vehicle_config_id is not None:
            try:
                myshop_vehicle_config_obj = MyShopVehicleConfig.objects.get(
                    pk=myshop_vehicle_config_id)
            except ObjectDoesNotExist:
                myshop_vehicle_config_obj = None
        myshop_vehicle_config_obj = None
        aa_instance = VehicleConfigMyShopConfig(
            vehicle_config_id=aa['VehicleConfigurationId'],
            myshop_vehicle_config=myshop_vehicle_config_obj,  # myshop_vehicle_config_id

        )
        aa_instance.save()


# vehicle into Vehicles_new_03 sql Table
# 2023-09-16 due to the vehicle_cust is blank. have to re-insert
# 2023-04-18 added a new section that allows to re-insert vehicle_make, vehicle_sub_model and etc. when a record is found.

model_name = 'Vehicle'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    data = json.load(f)
    # try:
    with transaction.atomic():  # wrap in a transaction
        for aa in data:
            if 'VehicleId' not in aa:
                logging.error(
                    f"Skipping entry due to missing 'VehicleId': {aa}")
                continue

            # Debugging
            # print(aa.get('VehicleId'), aa.get(
            #     'BrakeId'), type(aa.get('BrakeId')))
            # the .get() method will return None if the key is not found

            # Retrieve objects from dictionaries instead of DB queries
            vehicle_cust_obj = customer_dict.get(aa.get('CustId'))
            vehicle_make_obj = make_dict.get(aa.get('MakeId'))
            vehicle_submodel_obj = submodel_dict.get(aa.get('SubModelId'))
            vehicle_bodystyle_obj = bodystyle_dict.get(aa.get('BodyId'))
            vehicle_engine_obj = engine_dict.get(aa.get('EngineId'))
            vehicle_brake_obj = brake_dict.get(aa.get('BrakeId'))
            vehicle_transmission_obj = transmission_dict.get(
                aa.get('TransmissionId'))
            vehicle_GVW_obj = gvw_dict.get(aa.get('GVWId'))
            vehicle_drive_obj = drive_dict.get(aa.get('DriveTypeId'))
            vehicle_phone_obj = phone_dict.get(aa.get('DriverPhoneId'))
            vehicle_is_active = aa.get("Deleted") == 0

            # use update_or_create
            defaults = {
                'vehicle_year': aa['Year'],
                'vehicle_cust': vehicle_cust_obj,
                'vehicle_make': vehicle_make_obj,
                'vehicle_sub_model': vehicle_submodel_obj,
                'vehicle_body_style': vehicle_bodystyle_obj,
                'vehicle_engine': vehicle_engine_obj,
                'vehicle_transmission': vehicle_transmission_obj,
                'vehicle_brake': vehicle_brake_obj,
                'vehicle_drive_type': vehicle_drive_obj,
                'vehicle_gvw': vehicle_GVW_obj,
                'vehicle_odometer_1': aa['Odometer1'],
                'vehicle_odometer_2': aa['Odometer2'],
                'VIN_number': aa['Vin'],
                'vehicle_inspection_datetime': make_timezone_aware(aa['InspDate']),
                'vehicle_last_in_date': make_timezone_aware(aa['LastInDate']),
                'vehicle_license_plate_nbr': aa['License'],
                'vehicle_license_state': aa['LicenseState'],
                'vehicle_part_level': aa['PartLevel'],
                'vehicle_labor_level': aa['LaborLevel'],
                'vehicle_used_level': aa['UseVehicleLevels'],
                'vehicle_memo_01': aa['VehicleMemo'],
                'vehicle_memo_does_print_on_order': aa['VehicleMemoPrintOnOrder'],
                'vehicle_is_included_in_CRM_compaign': aa['IncludeInCRMCampaign'],
                'vehicle_color': aa['Color'],
                'vehicle_record_is_active': vehicle_is_active,
                'vehicle_class': aa['VehicleClass'],
                'vehicle_phone': vehicle_phone_obj,
                'vehicle_engine_hour_in': aa['EngineHoursIn'],
                'vehicle_engine_hour_out': aa['EngineHoursOut'],
                'vehicle_active_recall_counts': aa['ActiveRecallCount'],
                'vehicle_recall_last_checked_datetime': make_timezone_aware(aa['ActiveRecallLastChecked']),
                'vehicle_last_updated_at': aa['LastChangeDate'],
            }
            try:
                vehicle_instance, created = Vehicle.objects.update_or_create(
                    vehicle_id=aa['VehicleId'],
                    defaults=defaults
                )
                vehicle_instance.full_clean()
                vehicle_instance.save()
            except ValidationError as e:
                logging.error(
                    f"Validation error for Vehicle ID {aa['VehicleId']}: {e}")
                print(
                    f"Validation error for Vehicle ID {aa['VehicleId']}: {e}")

                raise
            except Exception as e:
                logging.error(
                    f"An error occurred while updating/creating Vehicle with ID {aa['VehicleId']}: {e}")
                print(
                    f"An error occurred while updating/creating Vehicle with ID {aa['VehicleId']}: {e}")

   

# vehiclenotes_new_03
model_name = 'VehicleNote'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    data = json.load(f)
    # try:
    with transaction.atomic():  # wrap in a transaction
        for aa in data:
            if 'VehicleId' not in aa:
                logging.error(
                    f"Skipping entry due to missing 'VehicleId': {aa}")
                continue

            # Debugging
            # print(aa.get('VehicleId'), aa.get(
            #     'BrakeId'), type(aa.get('BrakeId')))
            # the .get() method will return None if the key is not found

            # Retrieve objects from stored dictionaries instead of DB queries
            vehicle_obj = vehicle_dict.get(aa.get('VehicleId'))

            # use update_or_create
            defaults = {
                'vehicle': vehicle_obj,
                'vehicle_note_text': aa['NoteText'],
                'vehicle_note_last_updated_at ': aa['LastChangeDate'],
            }
            try:
                vehicle_note_instance, created = VehicleNotes.objects.update_or_create(
                    defaults=defaults
                )
                vehicle_note_instance.full_clean()
                vehicle_note_instance.save()
            except ValidationError as e:
                logging.error(
                    f"Validation error while adding notes for Vehicle ID {aa['VehicleId']}: {e}")
                print(
                    f"Validation error while adding notes for Vehicle ID {aa['VehicleId']}: {e}")

                raise
            except Exception as e:
                logging.error(
                    f"An error occurred while updating/creating a note for Vehicle with ID {aa['VehicleId']}: {e}")
                print(
                    f"An error occurred while updating/creating a note for Vehicle with ID {aa['VehicleId']}: {e}")

# AccountClass model into the accountclassess_new_03 table.
model_name = 'AccountClass'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    # when the file becomes big, break down into 1000 records per piece
    # added on 2023-04-10
    # while True:
    #     chunk = f.read(1000)
    #     if not chunk:
    #         break
    data_list = []
    data = json.load(f)
    for aa in data:

        aa_instance = AccountClass(
            account_class_id=aa['AccountClassId'],
            account_type=aa['AccountType'],
            account_last_updated_at=aa['LastChangeDate'],
        )
        # data_list.append(aa_instance)
        # Bulk create the repairorderLineItemSequence objects in the database
        # RepairOrderLineItem.objects.bulk_create(data_list)
        aa_instance.save()

#
model_name = 'InvoiceStatus'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    # when the file becomes big, break down into 1000 records per piece
    # added on 2023-04-10
    # while True:
    #     chunk = f.read(1000)
    #     if not chunk:
    #         break
    data_list = []
    data = json.load(f)
    for aa in data:

        aa_instance = InvoiceStatus(
            invoice_status_id=aa['InvoiceStatusId'],
            invoice_status_description=aa['Description'],
        )
        # data_list.append(aa_instance)
        # Bulk create the repairorderLineItemSequence objects in the database
        # RepairOrderLineItem.objects.bulk_create(data_list)
        aa_instance.save()


# CannedJobs into cannedjobs_new_03 sql Table
model_name = 'CannedJob'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    data = json.load(f)
    for aa in data:
        aa_instance = CannedJob(
            canned_job_id=aa['CannedJobId'],
            canned_job_title=aa['Name'],
            canned_job_description=aa['Description'],
            canned_job_is_in_quick_menu=aa['InQuickMenu'],
            canned_job_category_id=aa['CategoryId'],
            canned_job_applied_year=aa['Year'],
            canned_job_applied_make_id=aa['MakeId'],
            canned_job_applied_submodel_id=aa['SubModelId'],
            canned_job_vehicle_class=aa['VehicleClass'],
            canned_job_last_updated_at=aa['LastChangeDate'],
        )
        aa_instance.save()

# LineItem into lineitems_new_03 sql Table
model_name = 'LineItem'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    data = json.load(f)
    for aa in data:
        aa_instance = LineItem(
            line_item_id=aa['LineItemId'],
            line_item_account_class_id=aa['AcctClassId'],
            line_item_category_id=aa['CategoryId'],
            line_item_description=aa['Description'],
            line_item_cost=Decimal(aa['Cost']),
            line_item_sale=Decimal(aa['Sale']),
            line_item_is_tax_exempt=aa['TaxExempt'],
            line_item_has_no_commission=aa['NoCommission'],
            line_item_has_fixed_commission=aa['FixedCommission'],
            line_item_order_revision_id=aa['OrderRevisionId'],
            line_item_canned_job_id=aa['CannedJobId'],
            line_item_labor_sale=Decimal(aa['LaborSale']),
            line_item_part_sale=Decimal(aa['PartSale']),
            line_item_part_only_sale=Decimal(aa['PartOnlySale']),
            line_item_labor_only_sale=Decimal(aa['LaborOnlySale']),
            line_item_sublet_sale=aa['SubletSale'],
            line_item_package_sale=Decimal(aa['PackageSale']),
            line_item_tire_fee=Decimal(aa['TireFee']),
            line_item_parent_line_item_id=aa['ParentLineItemId'],
            line_item_last_updated_at=aa['LastChangeDate'],
        )
        aa_instance.save()

# LineItemTax into lineitemtaxes_new_03 sql Table
model_name = 'LineItemTaxes'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    data = json.load(f)
    for aa in data:
        aa_instance = LineItemTax(
            line_item_id=aa['LineItemId'],
            line_item_tax_id=aa['TaxId'],
            line_item_tax_charged=Decimal(aa['TaxCharged']),
            line_item_tax_rate=Decimal(aa['TaxRate']),
            line_item_tax_last_updated_at=aa['LastChangeDate'],
        )
        aa_instance.save()


# NoteItem into noteitems_new_03 sql Table
model_name = 'NoteItem'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    data = json.load(f)
    for aa in data:
        aa_instance = NoteItem(
            note_item_id=aa['NoteItemId'],
            line_item_id=aa['LineItemId'],
            note_text=(aa['NoteText']).strip(),
            is_printed_on_order=aa['PrintOnOrder'],
            tech_observation=aa['TechObservation'],
            note_item_last_updated_at=aa['LastChangeDate'],
        )
        aa_instance.save()


# part model into parts_new_03 sql Table
model_name = 'Part'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    data = json.load(f)
    for aa in data:
        aa_instance = Part(
            part_id=aa['PartId'],
            part_description=aa['Description'],
            part_cost=aa['Cost'],
            part_price=aa['Price'],
            part_is_tax_exempt=aa['TaxExempt'],
            part_category_id=aa['CategoryId'],
            part_account_class_id=aa['AccountClassId'],
            part_comments=aa['Comment'],
            part_manufacturer_id=aa['ManufacturerId'],
            part_list_price=aa['ListPrice'],
            part_is_user_entered_price=aa['UserEnteredPrice'],
            part_kit_id=aa['KitId'],
            part_is_MPLG_item=aa['IsMPLGItem'],
            part_is_changed_MPLG_item=aa['IsChangedMPLGItem'],
            part_is_core=aa['IsCore'],
            part_core_cost=aa['CoreCost'],
            part_core_list_price=aa['CoreListPrice'],
            part_fee_id=aa['PartFeeId'],
            part_is_deleted=aa['IsDeleted'],
            part_size=aa['Size'],
            part_is_tire=aa['IsTire'],
            part_last_updated_at=aa['LastChangeDate'],
        )
        aa_instance.save()


# partitem model into partitems_new_03 sql Table
model_name = 'PartItem'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    data = json.load(f)
    for aa in data:
        aa_instance = PartItem(
            part_item_id=aa['PartItemId'],
            line_item_id=aa['LineItemId'],
            part_discount_description_id=aa['PartDiscountDescriptionId'],
            part_item_is_user_entered_unit_sale=aa['IsUserEnteredUnitSale'],
            part_item_is_user_entered_unit_cost=aa['IsUserEnteredUnitCost'],
            part_item_quantity=aa['Quantity'],
            part_item_unit_price=aa['UnitPrice'],
            part_item_unit_list=aa['UnitList'],
            part_item_unit_sale=aa['UnitSale'],
            part_item_unit_cost=aa['UnitCost'],
            part_item_part_no=aa['PartNo'],
            part_item_part_id=aa['PartId'],
            part_item_is_confirmed=aa['IsConfirmed'],
            part_item_vendor_code=aa['VendorCode'],
            part_item_vendor_id=aa['VendorId'],
            part_item_manufacture_id=aa['ManufacturerId'],
            part_item_invoice_number=aa['InvoiceNumber'],
            part_item_commission_amount=aa['CommissionAmount'],
            part_item_is_committed=aa['IsCommitted'],
            part_item_is_quantity_confirmed=aa['IsQuantityConfirmed'],
            part_item_confirmed_quantity=aa['ConfirmedQuantity'],
            part_item_is_part_ordered=aa['IsPartOrdered'],
            part_item_is_core=aa['IsCore'],
            part_item_is_bundled_kit=aa['IsBundledKit'],
            part_item_is_MPlg_item=aa['IsMPlgItem'],
            part_item_is_changed_MPlg_item=aa['IsChangedMPlgItem'],
            part_item_part_type=aa['PartType'],
            part_item_size=aa['Size'],
            part_item_is_tire=aa['IsTire'],
            part_item_last_updated_at=aa['LastChangeDate'],
            part_item_meta=aa['Metadata'],
            part_item_added_from_supplier=aa['AddedFromSupplier'],
            part_item_purchased_from_vendor=aa['PurchasedFromVendor'],
            part_item_purchased_from_supplier=aa['PurchasedFromSupplier'],
            part_item_shipping_description=aa['ShippingDescription'],
            part_item_shipping_cost=aa['ShippingCost'],
        )
        aa_instance.save()

lineitem_dict = {
    lineitem.line_item_id: lineitem for lineitem in LineItem.objects.all()}
# LaborItem model to laboritems_new_03 sql table
model_name = 'LaborItem'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    data = json.load(f)
    for aa in data:
        line_item_id = aa['LineItemId']
        if line_item_id is not None:
            try:
                lineitem_obj = lineitem_dict.get(line_item_id)
            except ObjectDoesNotExist:
                lineitem_obj = LineItem.objects.get(pk=line_item_id)
        else:
            lineitem_obj = None

        # if LaborItem.objects.get(pk=aa['LaborItemId']) is not None:
        #     aa_instance = LaborItem.objects.get(pk=aa['LaborItemId'])
        #     if lineitem_obj is not None:
        #         aa_instance.line_item = lineitem_obj
        # else:
        aa_instance = LaborItem(
            labor_item_id=aa['LaborItemId'],
            line_item=lineitem_obj,
            labor_rate_description_id=aa['LaborRateDescriptionId'],
            labor_item_is_user_entered_labor_rate=aa['IsUserEnteredLaborRate'],
            labor_item_work_performed=aa['WorkPerformed'],
            labor_item_hours_charged=aa['HoursCharged'],
            labor_item_symptom=aa['Symptom'],
            labor_item_is_come_back_invoice=aa['ComeBackInvoice'],
            labor_item_parts_estimate=aa['PartsEstimate'],
            labor_item_is_MPlg_item=aa['IsMPlgItem'],
            labor_item_is_Changed_MPlg_item=aa['IsChangedMPlgItem'],
            labor_item_last_updated_at=aa['LastChangeDate'],
        )
        aa_instance.save()


# Make into makes_new_03 sql Table
model_name = 'Make'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    data = json.load(f)
    for aa in data:
        aa_instance = Make(
            make_id=aa['MakeId'],
            make_name=aa['Name'],

        )
        aa_instance.save()

# models into models_new_03 sql Table
model_name = 'Model'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    data = json.load(f)
    for aa in data:
        aa_instance = Model(
            model_id=aa['ModelId'],
            make_id=aa['MakeId'],
            model_name=aa['Name'],
        )
        aa_instance.save()

# models into models_new_03 sql Table
model_name = 'RepairOrderPhase'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    data = json.load(f)
    for aa in data:
        aa_instance = RepairOrderPhase(
            repair_order_phase_id=aa['RepairOrderPhaseId'],
            repair_order_phase_description=aa['Phase'],
        )
        aa_instance.save()

# insert repairorder into repairorders_new_03 sql table
# every time i add a new foreign key values into the original database, i need to reimport every time.
# it is time consuming given the 45-minute running time.

model_name = 'RepairOrder'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    data = json.load(f)
    for aa in data:
        # repair_order_phase, repair_order_customer and repair_order_vehicle are foreign keyf fields.
        phase_id = aa['RepairOrderPhaseId']
        customer_id = aa['CustId']
        vehicle_id = aa['VehicleId']
        if phase_id is not None:
            try:
                phase_obj = phase_dict.get(phase_id)
            except ObjectDoesNotExist:
                phase_obj = RepairOrderPhase.objects.get(pk=phase_id)
        else:
            phase_obj = None

        if customer_id is not None:
            try:
                customer_obj = customer_dict.get(customer_id)
            except ObjectDoesNotExist:
                customer_obj = Customer.objects.get(pk=customer_id)
        else:
            customer_obj = None

        if vehicle_id is not None:
            try:
                vehicle_obj = vehicle_dict.get(vehicle_id)
            except ObjectDoesNotExist:
                vehicle_obj = Vehicle.objects.get(pk=vehicle_id)
        else:
            vehicle_obj = None

        aa_instance = RepairOrder(
            repair_order_id=aa['RepairOrderId'],
            repair_order_phase=phase_obj,
            repair_order_customer=customer_obj,
            repair_order_vehicle=vehicle_obj,
            repair_order_serviced_vehicle_location=aa['Location'],
            repair_order_service_status=aa['StatusDescription'],
            repair_order_scheduled_start_datetime=parse_time(
                aa['ScheduleDate']),
            repair_order_billed_hours=Decimal(aa['ScheduledHours']),
            repair_order_promise_datetime=parse_time(aa['PromiseDate']),
            repair_order_is_printed=aa['RoPrinted'],
            repair_order_invoice_is_printed=aa['InvoicePrinted'],
            repair_order_serviced_vehicle_in_datetime=parse_time(aa['TimeIn']),
            repair_order_serviced_vehicle_out_datetime=parse_time(
                aa['TimeOut']),
            repair_order_serviced_vehicle_hat=aa['Hat'],
            repair_order_posted_datetime=parse_time(aa['DatePosted']),
            repair_order_serviced_vehicle_odometer_in=aa['OdometerIn'],
            repair_order_serviced_vehicle_odometer_out=aa['OdometerOut'],
            repair_order_reference_number=aa['ReferenceNumber'],
            repair_order_receipt_printed_datetime=parse_time(
                aa['PrintedDate']),  # aa['PrintedDate'],
            repair_order_snapshot_is_tax_exempt=aa['TaxExempt'],
            repair_order_aggr_notes=aa['Notes'],
            repair_order_observation_text_area=aa['Observations'],
            repair_order_created_as_estimate=aa['CreatedAsEstimate'],
            repair_order_snapshot_margin_pct=aa['MarginPct'],
            repair_order_snapshot_haz_waste_amount=Decimal(aa['HazWasteAmt']),
            repair_order_snapshot_labor_sale_amount=Decimal(aa['LaborSale']),
            repair_order_snapshot_parts_sale_amount=Decimal(aa['PartsSale']),
            repair_order_snapshot_supply_from_shop_amount=Decimal(
                aa['ShopSuppliesAmt']),
            repair_order_snapshot_tax_haz_material_amount=Decimal(
                aa['TaxAmtHazMat']),
            repair_order_snapshot_tax_supply_from_shop_amount=aa['TaxAmtShopSupplies'],
            repair_order_snapshot_total_tax_amount=Decimal(aa['TotalTaxAmt']),
            repair_order_snapshot_balance_due_adjusted=Decimal(
                aa['BalanceDueAdjustment']),
            repair_order_snapshot_discounted_amount=Decimal(aa['DiscountAmt']),
            repair_order_snapshot_part_discounted_desc_id=aa['PartDiscountDescriptionId'],
            repair_order_snapshot_labor_discounted_desc_id=aa['LaborRateDescriptionId'],
            repair_order_snapshot_order_total_amount=Decimal(aa['OrderTotal']),
            repair_order_snapshot_calc_haz_waste_cost=aa['CalculateHazWasteCost'],
            repair_order_snapshot_calc_shop_supply_cost=Decimal(
                aa['CalculateShopSuppliesCost']),
            repair_order_serviced_vehcle_engine_hours_in=Decimal(
                aa['EngineHoursIn']),
            repair_order_serviced_vehcle_engine_hours_out=Decimal(
                aa['EngineHoursOut']),
            repair_order_last_updated_at=parse_time(aa['LastChangeDate']),
            repair_order_appointment_request_uid=aa['AppointmentRequestUid'],
        )
        aa_instance.save()

# repairorderlineitem into repairorderlineitemsequences_new_03 sql Table

# manually way
model_name = 'RepairOrderLineItemSequence'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    # when the file becomes big, break down into 1000 records per piece
    # added on 2023-04-10
    # while True:
    #     chunk = f.read(1000)
    #     if not chunk:
    #         break
    data_list = []
    data = json.load(f)
    for aa in data:
        aa_instance = RepairOrderLineItem(
            ro_line_item_sequence_id=aa['RepairOrderLineItemSequenceId'],
            repair_order_id=aa['RepairOrderId'],
            line_item_id=aa['LineItemId'],
            sequence=aa['Sequence'],
            ro_line_item_sequence_last_updated_at=aa['LastChangeDate'],
        )
        # data_list.append(aa_instance)
        # Bulk create the repairorderLineItemSequence objects in the database
        # RepairOrderLineItem.objects.bulk_create(data_list)
        aa_instance.save()


# paymenttransactions into the paymenttransactions_new_03 table.
model_name = 'PaymentTransaction'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    # when the file becomes big, break down into 1000 records per piece
    # added on 2023-04-10
    # while True:
    #     chunk = f.read(1000)
    #     if not chunk:
    #         break
    data_list = []
    data = json.load(f)
    for aa in data:
        aa_instance = PaymentTransaction(
            payment_transaction_id=aa['PaymentTransactionId'],
            payment_last_updated_at=aa['LastChangeDate'],
        )
        # data_list.append(aa_instance)
        # Bulk create the repairorderLineItemSequence objects in the database
        # RepairOrderLineItem.objects.bulk_create(data_list)
        aa_instance.save()

customer_dict = {
    customer_obj.customer_id: customer_obj for customer_obj in Customer.objects.all()}
repairorder_dict = {
    repairorder_obj.repair_order_id: repairorder_obj for repairorder_obj in RepairOrder.objects.all()}
paymenttransaction_dict = {paymenttransaction_obj.payment_transaction_id:
                           paymenttransaction_obj for paymenttransaction_obj in PaymentTransaction.objects.all()}
invoice_status_dict = {invoice_status_obj.invoice_status_id:
                       invoice_status_obj for invoice_status_obj in InvoiceStatus.objects.all()}
account_class_dict = {account_class_obj.account_class_id:
                      account_class_obj for account_class_obj in AccountClass.objects.all()}

# payment into the payments_new_03 table.
model_name = 'Payment'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    # when the file becomes big, break down into 1000 records per piece
    # added on 2023-04-10
    # while True:
    #     chunk = f.read(1000)
    #     if not chunk:
    #         break
    data_list = []
    data = json.load(f)
    for aa in data:
        repair_order_id = aa['RepairOrderId']
        if repair_order_id is not None:
            try:
                repair_order_obj = repairorder_dict.get(repair_order_id)
            except ObjectDoesNotExist:
                repair_order_obj = RepairOrder.objects.get(pk=repair_order_id)
        else:
            repair_order_obj = None
        customer_id = aa['CustomerId']
        if customer_id is not None:
            try:
                customer_obj = customer_dict.get(customer_id)
            except ObjectDoesNotExist:
                customer_obj = Customer.objects.get(pk=customer_id)
        else:
            customer_obj = None
        payment_transction_id = aa['PaymentTransactionId']
        if payment_transction_id is not None:
            try:
                payment_transction_obj = paymenttransaction_dict.get(
                    payment_transction_id)
            except ObjectDoesNotExist:
                payment_transction_obj = PaymentTransaction.objects.get(
                    pk=payment_transction_id)
        else:
            payment_transction_obj = None
        invoice_status_id = aa['InvoiceStatusId']
        if invoice_status_id is not None:
            try:
                invoice_status_obj = invoice_status_dict.get(invoice_status_id)
            except ObjectDoesNotExist:
                invoice_status_obj = InvoiceStatus.objects.get(
                    pk=invoice_status_id)
        else:
            invoice_status_obj = None

        account_class_id = aa['AccountClassId']
        if account_class_id is not None:
            try:
                account_class_obj = account_class_dict.get(account_class_id)
            except ObjectDoesNotExist:
                account_class_obj = AccountClass.objects.get(
                    pk=account_class_id)
        else:
            account_class_obj = None

        aa_instance = Payment(
            payment_id=aa['PaymentId'],
            payment_repair_order=repair_order_obj,
            payment_record_number=aa['RecordNumber'],
            payment_customer=customer_obj,
            payment_date=aa['PaymentDate'],
            payment_check_data=aa['CheckData'],
            payment_auth_data=aa['AuthData'],
            payment_amount=aa['Amount'],
            payment_invoice_status=invoice_status_obj,
            payment_is_NSF=aa['IsNSF'],
            payment_is_NSF_reversal=aa['IsNSFReversal'],
            payment_is_fee_payment=aa['IsFeePayment'],
            payment_total_payment=aa['TotalPayment'],
            payment_deletion_date=aa['DeletionDate'],
            payment_transcation=payment_transction_obj,
            payment_account_class=account_class_obj,
            payment_verification_data=aa['VerificationData'],
            payment_receipt_one=aa['ReceiptOne'],
            payment_receipt_two=aa['ReceiptTwo'],
            payment_receipt_three=aa['ReceiptThree'],
            payment_last_updated_at=aa['LastChangeDate'],
        )
        # data_list.append(aa_instance)
        # Bulk create the repairorderLineItemSequence objects in the database
        # RepairOrderLineItem.objects.bulk_create(data_list)
        aa_instance.save()


# TextMessage model into the taxmessages_new_03 table.
model_name = 'TextMessage'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    # when the file becomes big, break down into 1000 records per piece
    # added on 2023-04-10
    # while True:
    #     chunk = f.read(1000)
    #     if not chunk:
    #         break
    data_list = []
    data = json.load(f)
    for aa in data:
        text_customer_id = aa['CustID']
        if text_customer_id is not None:
            text_customer_obj = customer_dict.get(text_customer_id)
        else:
            text_customer_obj = None

        aa_instance = TextMessage(
            text_message_id=aa['TextMessageId'],
            text_customer=text_customer_obj,
            text_body=aa['Body'],
            text_external_id=aa['ExternalId'],
            text_type=aa['Type'],
            text_to_phonenumber=aa['PhoneNumber'],
            text_direction=aa['Direction'],
            text_status=aa['Status'],
            text_error_message=aa['ErrorMessage'],
            text_error_code=aa['ErrorCode'],
            text_datetime=aa['Date'],
            text_body_size=aa['BodySize'],
            text_last_updated_at=aa['LastChangeDate'],
        )
        # data_list.append(aa_instance)
        # Bulk create the repairorderLineItemSequence objects in the database
        # RepairOrderLineItem.objects.bulk_create(data_list)
        aa_instance.save()

# --- read initial talent_management data

initial_data_filename = "2023-05-01-talent_management_init.csv"
initial_data_filepath = "/Users/stephenwang/Documents/myiCloudCopy-76ProLubePlus/13-Information-Technology/003-IT_New-Site-Development-2022/New_site_database-data-migration-python-scripts"
file_path = os.path.join(initial_data_filepath, initial_data_filename)

def csv_to_json(csv_full_path):
    with open(csv_full_path, 'r') as file:
        csv_data = csv.DictReader(file)
        json_data = json.dumps([row for row in csv_data])
    return json_data


# read the
json_data = csv_to_json(file_path)
print(json_data)

def convert_date_format(date_string):
    if date_string:
        # Convert the date string to a datetime object
        date_object = datetime.strptime(date_string, '%Y-%m-%d')

        # Convert the datetime object to the desired format
        converted_date = date_object.strftime('%Y-%m-%d')

        return converted_date
    else:
        converted_date = None
        return converted_date


data = json.loads(json_data)
for aa in data:

    aa_instance = Talent(
        talent_id=aa['talent_id'],
        talent_first_name=aa['talent_first_name'],
        talent_last_name=aa['talent_last_name'],
        talent_middle_name=aa['talent_middle_name'],
        talent_preferred_name=aa['talent_preferred_name'],
        talent_email=aa['talent_email'],
        talent_phone_number_primary=aa['talent_phone_number_primary'],
        talent_emergency_contact=aa['talent_emergency_contact'],
        talent_date_of_birth=aa['talent_date_of_birth'],
        talent_physical_address_01=aa['talent_physical_address_01'],
        talent_physical_address_02=aa['talent_physical_address_02'],
        talent_physical_address_city=aa['talent_physical_address_city'],
        talent_physical_address_state=aa['talent_physical_address_state'],
        talent_physical_address_zip_code=aa['talent_physical_address_zip_code'],
        talent_physical_address_country=aa['talent_physical_address_country'],
        talent_mailing_address_is_the_same_physical_address=aa[
            'talent_mailing_address_is_the_same_physical_address'],
        talent_mailing_address_01=aa['talent_mailing_address_01'],
        talent_mailing_address_02=aa['talent_mailing_address_02'],
        talent_mailing_address_city=aa['talent_mailing_address_city'],
        talent_mailing_address_state=aa['talent_mailing_address_state'],
        talent_mailing_address_zip_code=aa['talent_mailing_address_zip_code'],
        talent_mailing_address_country=aa['talent_mailing_address_country'],
        talent_education_level=aa['talent_education_level'],
        talent_certifications=aa['talent_certifications'],
        talent_hire_date=convert_date_format(aa['talent_hire_date']),
        talent_department=aa['talent_department'],
        talent_HR_remarks_json=aa['talent_HR_remarks_json'],
        talent_incident_record_json=aa['talent_incident_record_json'],
        talent_is_active=aa['talent_is_active'],
        talent_pay_type=aa['talent_pay_type'],
        talent_pay_rate=aa['talent_pay_rate'],
        talent_pay_frequency=aa['talent_pay_frequency'],
        talent_previous_department=aa['talent_previous_department'],
        talent_discharge_date=convert_date_format(aa['talent_discharge_date']),
        talent_years_of_work=aa['talent_years_of_work'],
        talent_supervisor_id=aa['talent_supervisor_id'],
    )
    # data_list.append(aa_instance)
    # Bulk create the repairorderLineItemSequence objects in the database
    # RepairOrderLineItem.objects.bulk_create(data_list)
    aa_instance.save()



# 2023-10-16
# adding CatalogLinks Data
model_name = 'CatalogLinks'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    primary_key_field = 'CatalogLink'
    data = json.load(f)
    # added on 2023-10-16 to clean extra spaces and empty strings
    data = clean_string_in_dictionary_object(data)
    # try:
    with transaction.atomic():  # wrap in a transaction
        for aa in data:
            if primary_key_field not in aa:
                logging.error(
                    f"Skipping vendor entry due to missing 'VendorId': {aa}")
                continue

            # Retrieve objects from dictionaries instead of DB queries
            catalog_link_id = aa.get(primary_key_field)
            vendor_type_obj = aa.get(aa.get('VendorTypeId'))

            # use update_or_create
            defaults = {
                'catelog_link_file_used': aa.get('Name'),
                'catelog_vendor_display_name': aa.get('Contact'),
                'catelog_vendor_[AuthCode]': aa.get('AuthCode'),

            }
            try:
                vendor, created = Vendors.objects.update_or_create(
                    vendor_id=vendor_id,
                    defaults=defaults
                )
                vendor.full_clean()
                vendor.save()

            except ValidationError as e:
                logging.error(
                    f"Validation error for Vendor ID {vendor_id}: {e}")
                print(
                    f"Validation error for Vendor ID {aa['VehicleId']}: {e}")

                raise
            except Exception as e:
                logging.error(
                    f"An error occurred while updating/creating Vendor with ID {vendor_id}: {e}")
                print(
                    f"An error occurred while updating/creating Vendor with ID {vendor_id}: {e}")


# 2023-10-16
# adding VendorType
model_name = 'VendorType'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    primary_key_field = 'VendorTypeId'
    data = json.load(f)
    # added on 2023-10-16 to clean extra spaces and empty strings
    data = clean_string_in_dictionary_object(data)
    # try:
    with transaction.atomic():  # wrap in a transaction
        for aa in data:
            if primary_key_field not in aa:
                logging.error(
                    f"Skipping vendor type entry due to missing '{primary_key_field}': {aa}")
                continue

            # Retrieve objects from dictionaries instead of DB queries
            vendor_type_id = aa.get(primary_key_field)

            # use update_or_create
            defaults = {
                'vendor_type_name': aa.get('Name'),
            }

            try:
                vendor_type, created = VendorTypes.objects.update_or_create(
                    vendor_type_id=vendor_type_id,
                    defaults=defaults,
                )
                vendor_type.full_clean()
                vendor_type.save()

            except ValidationError as e:
                logging.error(
                    f"Validation error for vendor_type ID {vendor_type_id}: {e}")
                print(
                    f"Validation error for vendor_type ID {vendor_type_id}: {e}")

                raise
            except Exception as e:
                logging.error(
                    f"An error occurred while updating/creating vendor_type ID {vendor_type_id}: {e}")
                print(
                    f"An error occurred while updating/creating vendor_type ID {vendor_type_id}: {e}")

# 2023-10-26 
# adding VendorAddresses
model_name = 'VendorAddresses'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
logger = logging.getLogger('django')

logger.info(f'Reading VendorAddresses data. source file: {file_path}')
with open(file_path, 'r') as f:
    primary_key_field = 'VendorId'
    data = json.load(f)
    # added on 2023-10-16 to clean extra spaces and empty strings
    data = clean_string_in_dictionary_object(data)
    # try:
    with transaction.atomic():  # wrap in a transaction
        for aa in data:
            if primary_key_field not in aa:
                logger.error(
                    f"Skipping vendor-address entry due to missing '{primary_key_field}': {aa}")
                continue

            # Retrieve objects from dictionaries instead of DB queries
            vendor_id = aa.get(primary_key_field)
            address_id = aa.get("AddressId")

            # use update_or_create
            # defaults = {
            #     'vendor_type_name': aa.get('Name'),
            # }

            try:
                vendor_address, created = VendorAdddresses.objects.update_or_create(
                    vendor_id=vendor_id,
                    address_id=address_id,

                )
                vendor_address.full_clean()
                vendor_address.save()

            except ValidationError as e:
                logging.error(
                    f"Validation error for vendor ID {vendor_id} and addresss ID {address_id}: {e}")
                print(
                    f"Validation error for vendoe ID {vendor_id} and addresss ID {address_id}: {e}")

                raise
            except Exception as e:
                logging.error(
                    f"An error occurred while updating/creating vendor ID {vendor_id} and addresss ID {address_id}: {e}")
                print(
                    f"An error occurred while updating/creating vendor ID {vendor_id} and addresss ID {address_id}: {e}")

# 2023-10-26 
# adding VendorLink
model_name = 'VendorLink'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
logger = logging.getLogger('django')

logger.info(f'Reading {model_name} data. source file: {file_path}')
print(f'Reading {model_name} data. source file: {file_path}')

with open(file_path, 'r') as f:
    primary_key_field = 'VendorId'
    data = json.load(f)
    # added on 2023-10-16 to clean extra spaces and empty strings
    data = clean_string_in_dictionary_object(data)
    # try:
    with transaction.atomic():  # wrap in a transaction
        for aa in data:
            if primary_key_field not in aa:
                logger.error(
                    f"Skipping vendor-address entry due to missing '{primary_key_field}': {aa}")
                continue

            vendor_id = aa.get(primary_key_field)
            vendor_link_property = aa.get("Property")
            vendor_link_value = aa.get("Value")

            # use update_or_create
            defaults = {
                'vendor_link_property':vendor_link_property,
                'vendor_link_value': vendor_link_value,
            }

            try:
                vendor_link, created = VendorLinks.objects.update_or_create(
                    vendor_id=vendor_id,
                    defaults=defaults,

                )
                vendor_link.full_clean()
                vendor_link.save()

            except ValidationError as e:
                logger.error(
                    f"Validation error for vendor ID {vendor_id}: {e}")
                print(
                    f"Validation error for vendor ID {vendor_id}: {e}")

                raise
            except Exception as e:
                logger.error(
                    f"An error occurred while updating/creating vendor ID {vendor_id}: {e}")
                print(
                    f"An error occurred while updating/creating vendor ID {vendor_id}: {e}")



# 2023-10-16
# adding Vendor model data
model_name = 'Vendor'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    primary_key_field = 'VendorId'
    data = json.load(f)
    # added on 2023-10-16 to clean extra spaces and empty strings
    data = clean_string_in_dictionary_object(data)
    # try:
    with transaction.atomic():  # wrap in a transaction
        for aa in data:
            if primary_key_field not in aa:
                logging.error(
                    f"Skipping vendor entry due to missing 'VendorId': {aa}")
                continue

            # Retrieve objects from dictionaries instead of DB queries
            vendor_id = aa.get(primary_key_field)
            vendor_type_obj = aa.get(aa.get('VendorTypeId'))
            vendor_catelog_link_obj = aa.get(aa.get('CatalogLinkId'))

            # use update_or_create
            defaults = {
                'vendor_name': aa.get('Name'),
                'vendor_contact_persons': aa.get('Contact'),
                'vendor_comment': aa.get('Comment'),
                'vendor_contact_email_address': aa.get('EmailAddress'),
                'vendor_code': aa.get('Code'),
                'vendor_limit': aa.get('Limit'),
                'vendor_terms': aa.get('Terms'),
                'vendor_acctount_class':aa.get('AcctClass'),
                'vendor_type vendor_type_obj':vendor_catelog_link_obj,
                'vendor_catelog_link': aa.get('CatalogLinkId'),
            }
            try:
                vendor, created = Vendors.objects.update_or_create(
                    vendor_id=vendor_id,
                    defaults=defaults
                )
                vendor.full_clean()
                vendor.save()

            except ValidationError as e:
                logging.error(
                    f"Validation error for Vendor ID {vendor_id}: {e}")
                print(
                    f"Validation error for Vendor ID {aa['VehicleId']}: {e}")

                raise
            except Exception as e:
                logging.error(
                    f"An error occurred while updating/creating Vendor with ID {vendor_id}: {e}")
                print(
                    f"An error occurred while updating/creating Vendor with ID {vendor_id}: {e}")
