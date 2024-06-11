# created on 2024-04-06 to generate QR code for inventory management.
# The QR code will contain the following information:
# 4-digit department_code, date_info, device_info, additional_info
from .base import HttpResponse, BytesIO, qrcode, render
from rest_framework import status
from django.contrib.contenttypes.models import ContentType
from qrcode.image.svg import SvgImage, SvgPathImage


def generate_qrcode_and_barcode_manual(request):
    if request.method == "POST":
        try:
            # Constructing data as a dictionary
            data = {
                'department_code': request.POST.get('department_code'),
                'date_info': request.POST.get('date_info'),
                'device_info': request.POST.get('device_info'),
                'additional_info': request.POST.get('additional_info'),
            }

            # Convert the dictionary to a string representation for the QR code
            data_str = '|'.join(f"{key}={value}" for key,
                                value in data.items() if value)

            qr = qrcode.QRCode(
                version=1,  # Adjust version based on the amount of data
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(data_str)
            qr.make(fit=True)

            img = qr.make_image(image_factory=SvgImage)

            response = HttpResponse(content_type='image/svg+xml')
            img.save(response)
            # img_io = BytesIO()
            # img.save(img_io, 'svg')
            # img_io.seek(0)
            # response.write(img_io.read())

            return response
        except Exception as e:
            # Log the error or send it to a monitoring system
            print(f"Error generating QR code: {e}")
            return HttpResponse('Error in generating QR code',
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:  # This will handle GET requests
        # Fetching specific models from different apps
        inventory_model = ContentType.objects.get(
            app_label='homepageapp', model='inventory')
        automan_inventory_model = ContentType.objects.get(
            app_label='homepageapp', model='automaninventory')
        part_model = ContentType.objects.get(
            app_label='homepageapp', model='partsmodel')
        # automan_part_model = ContentType.objects.get(
        #     app_label='homepageapp', model='automanpart')
        customer_model = ContentType.objects.get(
            app_label='homepageapp', model='customersnewsql02model')
        appointments_model = ContentType.objects.get(
            app_label='appointments', model='appointmentrequest')
        repair_order_model = ContentType.objects.get(
            app_label='homepageapp', model='repairordersnewsql02model')

        # Combining the models into a single list
        models_list = [inventory_model, part_model,
                       customer_model, appointments_model,
                       repair_order_model,
                       automan_inventory_model,
                       # automan_part_model
                       ]

        # Render a form template, passing the models_list as context
        return render(request, 'core_operations/40_generate_qrcode_and_barcode.html',
                      {'models_list': models_list})
