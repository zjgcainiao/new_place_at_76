from   .base import render

def payment_checkout_react(request):
    """
    Renders the payment checkout page for React app.
    """
    return render(request, 'shops/21_payment_checkout_react.html')