import hashlib
from .base import barcode, BytesIO
from barcode.writer import SVGWriter
from django.core.files.base import ContentFile
import uuid


def generate_code128_barcode_lite(product_id):
    """Generate a unique, efficient barcode based on the product_id with an additional random identifier."""
    try:
        # Create a random UUID to add randomness to the identifier
        # Take only the first 6 characters for brevity
        random_uuid = uuid.uuid4().hex[:6]

        # Create a hash object with a random secret key. 6 means 6 bytes long, whch is 12 digit alphanumeric.
        hash_object = hashlib.blake2b(key=b'Trump2024', digest_size=6)

        # Update the hash object with a combination of the product_id and random UUID
        combined_string = f"{product_id}{random_uuid}"
        hash_object.update(combined_string.encode('utf-8'))
        # Generate a hexadecimal digest
        hash_digest = hash_object.hexdigest()
        # Combine the  hash digest followed by the product_id (aka, the category, sku of the item) to form a unique code
        code = "-".join([hash_digest, product_id])

        # Generate barcode image using SVG format
        barcode_type = barcode.get_barcode_class('code128')  # Choosing Code128
        bar = barcode_type(code, writer=SVGWriter())

        # Save the barcode image to a BytesIO stream and then to a Django File
        svg_output = BytesIO()
        bar.write(svg_output)

        # Convert BytesIO to ContentFile which can be saved to a Django ImageField
        file_name = f'{code}.svg'
        content_file = ContentFile(svg_output.getvalue(), name=file_name)
    except Exception as e:
        raise Exception(f"Failed to generate SVG barcode for \
                        {product_id}: {str(e)}")

    return code, content_file
