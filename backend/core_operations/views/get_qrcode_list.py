from core_operations.models import GeneratedQRCode
from .base import render


def get_qrcode_list(request):
    """
    List all QR codes generated
    """
    # Fetch all the QR codes from the database
    qrcodes = GeneratedQRCode.objects.filter(
        is_active=True).order_by('-created_at')

    return render(request, 'core_operations/41_qrcode_list.html', {'qrcodes': qrcodes})
