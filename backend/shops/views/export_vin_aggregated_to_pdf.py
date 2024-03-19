import aiohttp
from rest_framework.request import Request
from django.http import JsonResponse
from .base import render, database_sync_to_async, \
    io, canvas, letter, HttpResponse
from apis.serializers import VinDataAggregatedSerializer
from apis.views import VinDataAggregatedViewSet
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.urls import reverse
from django.conf import settings
from urllib.parse import urljoin


async def export_vin_aggregated_to_pdf(request):
    """
    Exports the VIN data to a PDF file.
    """
    vin = request.GET.get('vin', None)
    if not vin:
        return JsonResponse({"error": "VIN not provided"}, status=400)
    # Determine the base URL based on DEBUG setting
    base_url = 'http://127.0.0.1:8000' if settings.DEBUG else 'https://www.new76prolubeplus.com'

    # Dynamically generate the endpoint URL
    endpoint_path = "apis/vin_data_aggregated/search_by_vin/"

    # Construct the full URL
    search_url = urljoin(base_url, endpoint_path) + f"?format=json&vin={vin}"

    async with aiohttp.ClientSession() as session:
        async with session.get(search_url) as response:
            if response.status != 200:
                return JsonResponse({"error": "Failed to retrieve data"}, status=response.status)
            vin_data = await response.json()

    if not vin_data or not isinstance(vin_data, dict):
        return JsonResponse({"error": "No valid data found for the provided VIN"}, status=404)

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textobject = c.beginText(40, 50)  # Start near the top of the page
    y_position = 50  # Initial Y position

    # Define the page top margin threshold for adding a new page
    page_top_margin_threshold = 750  # Adjust this based on your page size

    for section, items in vin_data.items():
        if items is None:
            continue

        # Check if we need to add a new page
        if y_position > page_top_margin_threshold:
            c.drawText(textobject)
            c.showPage()
            textobject = c.beginText(40, 50)
            y_position = 50
        textobject.setTextOrigin(40, y_position)
        textobject.textLine(f"{section.capitalize()}:")
        y_position += 15  # Adjust Y position for the next line
        process_items(textobject, items, y_position,
                      page_top_margin_threshold, c)

    # Finish up the current page
    c.drawText(textobject)
    c.showPage()
    c.save()
    buf.seek(0)

    # Return the response with the PDF file
    response = HttpResponse(buf.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{vin}_report.pdf"'
    return response


def process_items(textobject, items, y_position, threshold, canvas):
    if isinstance(items, list):
        for item in items:
            if y_position > threshold:
                canvas.drawText(textobject)
                canvas.showPage()
                textobject = canvas.beginText(40, 40)
                y_position = 50

            textobject.setTextOrigin(40, y_position)
            if isinstance(item, dict):
                for key, value in item.items():
                    textobject.textLine(
                        f"    {key}: {value if value is not None else 'N/A'}")
                    y_position += 15
                    if y_position > threshold:
                        canvas.drawText(textobject)
                        canvas.showPage()
                        textobject = canvas.beginText(40, 50)
                        y_position = 50
            else:
                textobject.textLine(f"    {item}")
                y_position += 15
    elif isinstance(items, dict):
        for key, value in items.items():
            if y_position > threshold:
                canvas.drawText(textobject)
                canvas.showPage()
                textobject = canvas.beginText(40, 50)
                y_position = 50

            textobject.setTextOrigin(40, y_position)
            textobject.textLine(
                f"    {key}: {value if value is not None else 'N/A'}")
            y_position += 15
    else:
        if y_position > threshold:
            canvas.drawText(textobject)
            canvas.showPage()
            textobject = canvas.beginText(40, 50)
            y_position = 50

        textobject.setTextOrigin(40, y_position)
        textobject.textLine(f"    {items}")
        y_position += 15
