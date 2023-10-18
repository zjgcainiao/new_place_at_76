from django.shortcuts import render, redirect
import stripe


# standard django based checkout page, using ES6 module based stripe.js
def payment_checkout(request):
    return render(request, 'shops/21_payment_checkout.html')

# react app based checkout.


def payment_checkout_react(request):
    return render(request, 'shops/21_payment_checkout_react.html')

# backend stripe charge function


def stripe_charge(request):
    if request.method == 'POST':
        token = request.POST['stripeToken']
        stripe.Charge.create(
            amount=1000,  # amount in cents
            currency='usd',
            description='A description',
            source=token,
        )
        return redirect('some_view_name')
