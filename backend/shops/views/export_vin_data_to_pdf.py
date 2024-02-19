from .base import render, database_sync_to_async, HttpResponse, \
    io, canvas, letter, HttpResponse


async def export_vin_data_to_pdf(request):
    """
    Exports the VIN data to a PDF file.
    """
    latest_vin_data = await database_sync_to_async(request.session.get)('latest_vin_data')

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    y_position = 72

    for entry in latest_vin_data:
        c.drawString(72, y_position, f"{entry['key']}: {entry['value']}")
        y_position += 15

    c.showPage()
    c.save()
    buf.seek(0)

    return HttpResponse(buf.getvalue(), content_type='application/pdf')