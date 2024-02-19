from .base import stripe, redirect

def stripe_charge(request):
    """
    Handles the Stripe charge request.
    """
    if request.method == 'POST':
        token = request.POST['stripeToken']
        stripe.Charge.create(
            amount=1000,  # amount in cents
            currency='usd',
            description='A description',
            source=token,
        )
        return redirect('some_view_name')