from .base import JsonResponse, stripe, logger


# when a product
def create_payment_intent(request, product_id):
    """
    Creates a payment intent for the specified product.
    """
    try:

        # Assuming 'payment_intent_id' is stored in the session
        existing_intent_id = request.session.get('payment_intent_id')

        # Retrieve and validate existing intent if available
        if existing_intent_id:
            try:
                intent = stripe.PaymentIntent.retrieve(existing_intent_id)
                # Check if the intent is still usable (e.g., not succeeded, not expired)
                if intent.status in ['requires_payment_method', 'requires_confirmation']:
                    return JsonResponse({'clientSecret': intent.client_secret,
                                         'paymentIntentId': intent.id,

                                         })
            except stripe.error.InvalidRequestError:
                # Handle case where intent does not exist or is not retrievable
                pass  # Proceed to create a new intent below

        # Retrieve the product's price from Stripe
        # Assuming each product has a single price associated with it
        prices = stripe.Price.list(product=product_id, active=True, limit=1)

        if not prices.data:
            return JsonResponse({'error': 'Price not found for the specified product.'}, status=404)
        
        price = prices.data[0].unit_amount  # Price in cents
        intent = stripe.PaymentIntent.create(
            amount=price,
            currency="usd",
            automatic_payment_methods={"enabled": True},
        )
        # Store the new payment intent ID in the session
        request.session['payment_intent_id'] = intent.id

        return JsonResponse(
            {'clientSecret': intent.client_secret,
             'paymentIntentId': intent.id,
             })
    except Exception as e:
        return JsonResponse({'error': f'{e}'}, status=403)