# this seralizers.py is to import data in json

import json
import os
from decimal import Decimal, ROUND_HALF_UP
from homepageapp.models import EmailsNewSQL02Model as Email, CustomersNewSQL02Model as Customer
from homepageapp.models import AddressesNewSQL02Model as Address, PhonesNewSQL02Model as Phone, VehiclesNewSQL02Model as Vehicle
from homepageapp.models import CustomerAddressesNewSQL02Model as CustomerAddress
from homepageapp.models import CannedJobsNewSQL02Model as CannedJob, LineItemsNewSQL02Model as LineItem
from homepageapp.models import lineItemTaxesNewSQL02Model as LineItemTax, NoteItemsNewSQL02Model as NoteItem
from homepageapp.models import RepairOrderPhasesNewSQL02Model as RepairOrderPhase, RepairOrdersNewSQL02Model as RepairOrder
from homepageapp.models import RepairOrderLineItemSquencesNewSQL02Model as RepairOrderLineItem
from homepageapp.models import MakesNewSQL02Model as Make, ModelsNewSQL02Model as Model
from homepageapp.models import AccountClassModel as AccountClass, PaymentsModel as Payment, PaymentTransactionsModel as PaymentTransaction

module_dir = '/Users/stephenwang/Documents/myiCloudCopy-76ProLubePlus/13-Information-Technology/003-IT_New-Site-Development-2022/New_site_database-data-migration-python-scripts/old_db_jsons'
suffix_pattern = '_20230115.json'

# def testing(request):
# Addresses into Addressess_new_03 sql Table
model_name = 'Addresses'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    data = json.load(f)
    for aa in data:
        aa_instance = Address(
            address_id = aa['AddressId'],
            address_type_id = aa['AddressTypeId'],
            address_company_or_ATTN = aa['Company'],
            address_line_01 = aa['Address'],
            address_city = aa['City'],
            address_state = aa['State'],
            address_zip_code = aa['ZipCode'],
            address_last_updated_date = aa['LastChangeDate'],
        )
        aa_instance.save()

# customer into customers_new_03 sql table
model_name = 'Customer'
file_path = os.path.join(module_dir, (model_name + suffix_pattern))
with open(file_path, 'r') as f:
    customer_data = json.load(f)
    for aa in customer_data:
        aa_instance = Customer(
            customer_id = aa['CustId'],
            customer_title_id = aa['TitleId'],
            customer_first_name = aa['FirstName'],
            customer_last_name = aa['LastName'],
            customer_dob = aa['DOB'],
            customer_spouse_name = aa['SpouseName'],
            customer_is_okay_to_charge = aa['ChargeOK'],
            customer_memo_1 = aa['Remarks'],
            customer_resale_permit_nbr = aa['ResaleNum'],
            customer_is_in_social_crm = aa['IncludeInCRMCampaign'],
            customer_is_tax_exempt = aa['TaxExempt'],
            customer_last_visit_date = aa['LastVisited'],
            customer_first_visit_date = aa['FirstVisited'],
            customer_hear_from_us_type = aa['RefTypeId'],
            customer_is_deleted = aa['IsDeleted'],
            customer_is_created_from_appointments = aa['IsFromSchedule'],
            customer_does_allow_SMS = aa['SMSAllowed'],
            customer_email_address_in_json = aa['EmailAddress'],
            customer_last_updated_date = aa['LastChangeDate'],
            customer_fleet_vendor_id = aa['FleetVendorId'],  
            # customer_memo_1 = '' # empty string for the field.
        )
        aa_instance.save()

# Email to emails_new_03 sql table   
file_path = os.path.join(module_dir, 'Email'+suffix_pattern)
with open(file_path, 'r') as f:
    email_data = json.load(f)
    for aa in email_data:
        aa_instance = Email(
        email_id = aa['Id'],
        email_type_id = aa['EmailTypeId'],
        email_address = aa['Email'],
        email_description = aa['Description'],
        email_last_updated_date = aa['LastChangeDate']
        )
        aa_instance.save()

# phone model into Phones_new_03 sql table
file_path = os.path.join(module_dir, 'PhoneNum' + suffix_pattern)
with open(file_path, 'r') as f:
    data = json.load(f)
    for aa in data:
        aa_instance = Phone(
            phone_id = aa['PhoneId'],
            phone_desc_id = aa['PhoneDescId'],
            phone_number = aa['PhoneNum'],
            phone_number_ext = aa['Ext'],
            phone_displayed_name = aa['Display'],
            phone_memo_01 = aa['Note'],
            phone_last_updated_date = aa['LastChangeDate'],

        )
        aa_instance.save()


# vehicle into Vehicles_new_03 sql Table
model_name = 'Vehicle'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    data = json.load(f)
    for aa in data:
        aa_instance = Vehicle(
            vehicle_id = aa['VehicleId'],
            vehicle_cust_id = aa['CustId'],
            vehicle_year = aa['Year'],
            vehicle_make_id = aa['MakeId'],
            vehicle_sub_model_id = aa['SubModelId'],
            vehicle_body_style_id = aa['BodyId'],
            vehicle_engine_id = aa['EngineId'],
            vehicle_transmission_id = aa['TransmissionId'],
            vehicle_brake_id = aa['BrakeId'],
            vehicle_drive_type_id = aa['DriveTypeId'],
            vehicle_GVW_id = aa['GVWId'],
            vehicle_odometer_1 = aa['Odometer1'],
            vehicle_odometer_2 = aa['Odometer2'],
            VIN_number = aa['Vin'],
            vehicle_inspection_datetime = aa['InspDate'],
            vehicle_last_in_date = aa['LastInDate'],
            vehicle_license_plate_nbr = aa['License'],
            vehicle_license_state = aa['LicenseState'],
            vehicle_part_level = aa['PartLevel'],
            vehicle_labor_level = aa['LaborLevel'],
            vehicle_used_level = aa['UseVehicleLevels'],
            vehicle_memo_01 = aa['VehicleMemo'],
            vehicle_memo_does_print_on_order = aa['VehicleMemoPrintOnOrder'],
            vehicle_is_included_in_CRM_compaign = aa['IncludeInCRMCampaign'],
            vehicle_color = aa['Color'],
            vehicle_record_is_activate = aa['Deleted'],
            vehicle_class_id = aa['VehicleClass'],
            vehicle_phone_id = aa['DriverPhoneId'],
            vehicle_engine_hour_in = aa['EngineHoursIn'],
            vehicle_engine_hour_out = aa['EngineHoursOut'],
            vehicle_active_recall_counts = aa['ActiveRecallCount'],
            vehicle_recall_last_checked_datetime = aa['ActiveRecallLastChecked'],
            vehicle_last_updated_datetime = aa['LastChangeDate'],

        )
        aa_instance.save()



# CustomerAddresses into CustomerAddressess_new_03 sql Table
model_name = 'CustomerAddresses'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    data = json.load(f)
    for aa in data:
        aa_instance = CustomerAddress(
            address_id = aa['AddressId'],
            customer_id = aa['CustID'],
            customeraddress_last_updated_date = aa['LastChangeDate'],

        )
        aa_instance.save()

# CannedJobs into cannedjobs_new_03 sql Table
model_name = 'CannedJob'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    data = json.load(f)
    for aa in data:
        aa_instance = CannedJob(
            canned_job_id = aa['CannedJobId'],
            canned_job_title = aa['Name'],
            canned_job_description = aa['Description'],
            canned_job_is_in_quick_menu = aa['InQuickMenu'],
            canned_job_category_id = aa['CategoryId'],
            canned_job_applied_year = aa['Year'],
            canned_job_applied_make_id = aa['MakeId'],
            canned_job_applied_submodel_id = aa['SubModelId'],
            canned_job_vehicle_class = aa['VehicleClass'],
            canned_job_last_updated_date = aa['LastChangeDate'],
        )
        aa_instance.save()

# LineItem into lineitems_new_03 sql Table
model_name = 'LineItem'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    data = json.load(f)
    for aa in data:
        aa_instance = LineItem(
            line_item_id = aa['LineItemId'],
            line_item_account_class_id = aa['AcctClassId'],
            line_item_category_id = aa['CategoryId'],
            line_item_description = aa['Description'],
            line_item_cost = Decimal(aa['Cost']),
            line_item_sale = Decimal(aa['Sale']),
            line_item_is_tax_exempt = aa['TaxExempt'],
            line_item_has_no_commission = aa['NoCommission'],
            line_item_has_fixed_commission = aa['FixedCommission'],
            line_item_order_revision_id = aa['OrderRevisionId'],
            line_item_canned_job_id = aa['CannedJobId'],
            line_item_labor_sale = Decimal(aa['LaborSale']),
            line_item_part_sale = Decimal(aa['PartSale']),
            line_item_part_only_sale = Decimal(aa['PartOnlySale']),
            line_item_labor_only_sale = Decimal(aa['LaborOnlySale']),
            line_item_sublet_sale = aa['SubletSale'],
            line_item_package_sale = Decimal(aa['PackageSale']),
            line_item_tire_fee = Decimal(aa['TireFee']),
            line_item_parent_line_item_id = aa['ParentLineItemId'],
            line_item_last_updated_date = aa['LastChangeDate'],
        )
        aa_instance.save()



# LineItemTax into lineitemtaxes_new_03 sql Table
model_name = 'LineItemTaxes'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    data = json.load(f)
    for aa in data:
        aa_instance = LineItemTax(
            line_item_id = aa['LineItemId'],
            line_item_tax_id = aa['TaxId'],
            line_item_tax_charged = Decimal(aa['TaxCharged']),
            line_item_tax_rate = Decimal(aa['TaxRate']),
            line_item_tax_last_updated_date = aa['LastChangeDate'],
        )
        aa_instance.save()



# NoteItem into noteitems_new_03 sql Table
model_name = 'NoteItem'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    data = json.load(f)
    for aa in data:
        aa_instance = NoteItem(
            note_item_id = aa['noteItemId'],
            line_item_id = aa['LineItemId'],
            note_text = (aa['NoteText']).strip(),
            is_printed_on_order = aa['PrintOnOrder'],
            tech_observation = aa['TechObservation'],
            note_item_last_updated_date = aa['LastChangeDate'],
            
            )
        aa_instance.save()


# Make into makes_new_03 sql Table
model_name = 'Make'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    data = json.load(f)
    for aa in data:
        aa_instance = Make(

            make_id = aa['MakeId'],
            make_name = aa['Name'],

        )
        aa_instance.save()

# models into models_new_03 sql Table
model_name = 'Model'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    data = json.load(f)
    for aa in data:
        aa_instance = Make(

        model_id = aa['ModelId:'],
        make_id = aa['MakeId:'],
        model_name = aa['Name:'],

        )
        aa_instance.save()

# repairorder into repairorders_new_03 sql Table
model_name = 'RepairOrder'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    data = json.load(f)
    for aa in data:
        aa_instance = RepairOrder(
            repair_order_serviced_vehicle_out_datetime  = aa['TimeOut'],
            repair_order_serviced_vehicle_hat  = aa['Hat'],
            repair_order_posted_datetime = aa['DatePosted'],
            repair_order_serviced_vehicle_odometer_in = aa['OdometerIn '],
            repair_order_serviced_vehicle_odometer_out = aa['OdometerOut'],
            repair_order_reference_number = aa['ReferenceNumber'],
            repair_order_receipt_printed_datetime = aa['PrintedDate '],
            repair_order_snapshot_is_tax_exempt = aa['TaxExempt'],
            repair_order_aggr_notes = aa['Notes'],
            repair_order_observation_text_area = aa['Observations'],
            repair_order_created_as_estimate = aa['CreatedAsEstimate'],
            repair_order_snapshot_margin_pct = aa['MarginPct'],
            repair_order_snapshot_haz_waste_amount = aa['HazWasteAmt'],
            repair_order_snapshot_labor_sale_amount  = aa['LaborSale'],
            repair_order_snapshot_parts_sale_amount  = aa['PartsSale'],
            repair_order_snapshot_supply_from_shop_amount  = aa['ShopSuppliesAmt'],
            repair_order_snapshot_tax_haz_material_amount  = aa['TaxAmtHazMat'],
            repair_order_snapshot_tax_supply_from_shop_amount  = aa['TaxAmtShopSupplies'],
            repair_order_snapshot_total_tax_amount  = aa['TotalTaxAmt'],
            repair_order_snapshot_balance_due_adjusted = aa['BalanceDueAdjustment'],
            repair_order_snapshot_discounted_amount = aa['DiscountAmt'],
            repair_order_snapshot_part_discounted_desc_id = aa['PartDiscountDescriptionId'],
            repair_order_snapshot_labor_discounted_desc_id  = aa['LaborRateDescriptionId'],
            repair_order_snapshot_order_total_amount  = aa['OrderTotal'],
            repair_order_snapshot_calc_haz_waste_cost  = aa['CalculateHazWasteCost'],
            repair_order_snapshot_calc_shop_supply_cost  = aa['CalculateShopSuppliesCost'],
            repair_order_serviced_vehcle_engine_hours_in = aa['EngineHoursIn'],
            repair_order_serviced_vehcle_engine_hours_out  = aa['EngineHoursOut'],
            repair_order_last_updated_date = aa['LastChangeDate'],
            repair_order_appointment_request_uid = aa['AppointmentRequestUid'],
        )
        aa_instance.save()

# repairorderlineitem into repairorderlineitemsequences_new_03 sql Table
model_name = 'RepairOrderLineItemSequence'
file_path = os.path.join(module_dir, model_name + suffix_pattern)
with open(file_path, 'r') as f:
    data = json.load(f)
    for aa in data:
        aa_instance = RepairOrderLineItem(
            ro_line_item_sequence_id = aa['RepairOrderLineItemSequenceId'],
            repair_order_id = aa['RepairOrderId'],
            line_item_id = aa['LineItemId'],
            sequence = aa['Sequence'],
            ro_line_item_sequence_last_updated_date = aa['LastChangeDate'],
        )
        aa_instance.save()

