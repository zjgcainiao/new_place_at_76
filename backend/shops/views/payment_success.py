from .base import render


def payment_success(request):
    """
    Renders the payment success page.
    """
    return render(request, 'shops/30_payment_success.html')