import barcode
from barcode.writer import SVGWriter
from io import BytesIO
from django.core.files.base import ContentFile

# this is reserved for code128 based barcode for internal inventory rack system


def generate_code128_barcode(code):
    try:
        # Using Code 128 which includes its own error correction mechanisms
        barcode_class = barcode.get_barcode_class('code128')
        barcode_writer = SVGWriter()

        # Generate barcode
        barcode_obj = barcode_class(code, writer=barcode_writer)

        # Save barcode to a BytesIO buffer
        buffer = BytesIO()
        barcode_obj.write(buffer)

        # Return the SVG content as a Django File
        return ContentFile(buffer.getvalue(), name=f"{code}.svg")
    except Exception as e:
        raise Exception(
            f"Failed to generate SVG barcode for {code}: {str(e)}")

# Example usage in a Django model or view
# barcode_file = generate_high_quality_code128('FILTER-AF-MF03847')
