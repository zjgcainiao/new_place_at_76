from barcode.upc import UniversalProductCodeA
from core_operations.models import GeneratedBarCode
from barcode.writer import SVGWriter
from io import BytesIO
from core_operations.constants import GS1_COMPANY_PREFIX
from django.db import transaction
from django.core.files.base import ContentFile
# UPC-A barcode: 12 digits
# 2024-04-23
# a product_number defines a product to sell


def generate_upc_barcode(product_number):

    gs1_company_prefix = GS1_COMPANY_PREFIX
    # NG means Nitrile Mechanic Gloves
    product_number = '81803'

    string = f"{gs1_company_prefix}{product_number}".zfill(11)

    upca = UniversalProductCodeA(string, writer=SVGWriter())

    svg_bytes = BytesIO()
    if upca.calculate_checksum():
        upca.write(svg_bytes)
        full_code = upca.get_fullcode()
        svg_bytes_content = ContentFile(
            svg_bytes.getvalue(), name=f'{full_code}.svg')

        with transaction.atomic():
            barcode = GeneratedBarCode.objects.update_or_create(
                full_code=full_code,
                defaults={
                    'image': svg_bytes_content
                }
            )
