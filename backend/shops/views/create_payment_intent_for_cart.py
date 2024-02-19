from .base import stripe, redirect, render, JsonResponse

def create_payment_intent_for_cart(request):
    if request.method == "POST":
        try:
            # Example: Fetch cart items from session or database
            cart_items = request.session.get('cart', [])
            # Calculate total amount (in cents)
            total_amount = sum(item['price'] * item['quantity'] for item in cart_items)

            # Create a Stripe PaymentIntent
            intent = stripe.PaymentIntent.create(
                amount=total_amount,
                currency="usd",
                automatic_payment_methods={"enabled": True},
            )

            # Optionally, save the payment intent ID in the session for later use
            request.session['payment_intent_id'] = intent['id']

            # Redirect to a new page to complete payment
            return redirect('complete_payment', client_secret=intent['client_secret'])
        except Exception as e:
            # Handle errors
            return JsonResponse({'error': str(e)}, status=400)
    else:
        # Show the cart page with checkout button
        return render(request, 'cart_page.html')