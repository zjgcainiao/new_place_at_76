from .base import render, logger, redirect
from shops.models import UserVINAccess, Vin
from django.contrib import messages


def payment_success(request):
    """
    Renders the payment success page.
    """
    # Retrieve vin from session
    vin = request.session.get("vin_to_checkout")
    if not vin:
        # Handle case where vin is not found in session
        # Redirect or display an error message
        messages.error(
            request, "Somthing went wrong. We cannot find the vin related to your purchase. Please try again and ensure to ensure cookies are enabled.")
        return redirect('shops:vehicle_search_product')
    logger.info(f'suceessfully retrieved vin_to_purchase {vin} from session')
    # Retrieve additional data as needed for UserVINAccess
    email = request.user.email  # Assuming user is authenticated
    vin = Vin.objects.get(vin=vin)  # Assuming Vin model exists

    # Create UserVINAccess instance
    user_vin_access, created = UserVINAccess.objects.update_or_create(
        email=email,
        vin=vin,
        is_paid=True,
        # Replace with actual payment intent ID from Stripe
        payment_intent_id="stripe_payment_intent_id"
    )
    logger.info(f'suceessfully retrieved vin_to_purchase {vin} from session')
    # Clear the vin from session
    del request.session['vin_to_checkout']
    context = {
        'vin': vin,
        'user_vin_access': user_vin_access,
    }
    # Return response or render a success pa
    return render(request, 'shops/30_payment_success.html', context)
