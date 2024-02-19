from .base import render

def payment_cancelled(request):
    """
    Renders the payment cancelled page.
    """
    return render(request, 'shops/31_payment_cancelled.html')