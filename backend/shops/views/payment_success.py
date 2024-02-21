from .base import render
from shops.models import UserVINAccess, Vin

def payment_success(request):
    """
    Renders the payment success page.
    """
     # Retrieve vin from session
    vin = request.session.get("vin")
    if not vin:
        # Handle case where vin is not found in session
        # Redirect or display an error message
        return render(request, "error.html")
    
    # Retrieve additional data as needed for UserVINAccess
    email = request.user.email  # Assuming user is authenticated
    vin = Vin.objects.get(vin=vin)  # Assuming Vin model exists
    
    # Create UserVINAccess instance
    user_vin_access = UserVINAccess.objects.create(
        email=email,
        vin=vin,
        is_paid=True,
        payment_intent_id="stripe_payment_intent_id"  # Replace with actual payment intent ID from Stripe
    )
    
    # Clear the vin from session
    del request.session['vin']
    
    # Return response or render a success pa
    return render(request, 'shops/30_payment_success.html')