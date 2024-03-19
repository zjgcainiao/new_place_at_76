from .base import render, redirect, JsonResponse, stripe, settings, reverse, \
    logger, timezone, messages
from urllib.parse import urljoin
from django.contrib.sites.shortcuts import get_current_site
from stripe.error import InvalidRequestError


def prebuilt_checkout(request, *args, **kwargs):
    """
    Renders the prebuilt checkout page for the specified product.
    """
    # Fetch vin from query parameters, defaulting to None if not provided
    vin = request.GET.get('vin', None)
    if vin is None:
        messages.info(request, 'use the following form to start with.')
        # Redirect to a page where the user can enter the VIN
        return redirect('shops:vehicle_search_product')
    # Determine the domain based on DEBUG setting
    # MY_DOMAIN = f'http://{current_site.domain}' if settings.DEBUG else f'https://{current_site.domain}'
    MY_DOMAIN = 'http://127.0.0.1:8000/' if settings.DEBUG else 'https://www.new76prolubeplus.com/'
    # defaut product_id
    product_id = 'prod_PKOol19RtrtGTG'
    logger.info(f'using default product_id on prebuilt_checkout view...')

    if not request.session.get('vin_to_checkout'):
        request.session['vin_to_checkout'] = vin
    # Retrieve existing checkout session ID from session, if any
    existing_checkout_session_id = request.session.get('checkout_session_id')
    if existing_checkout_session_id:
        try:
            checkout_session = stripe.checkout.Session.retrieve(
                existing_checkout_session_id)
            # Redirect to existing checkout session if it's still active
            if checkout_session.payment_status in ['unpaid', 'requires_payment_method'] and checkout_session.status in ['open',]:
                logger.info(
                    f'Redirecting to existing checkout session {existing_checkout_session_id}...')
                return redirect(checkout_session.url, code=303)
        except InvalidRequestError as e:
            logger.error(f'InvalidRequestError: {str(e)}')
            # Clear the invalid session ID
            del request.session['checkout_session_id']

    # Fetch the product's price
    try:
        prices = stripe.Price.list(product=product_id, active=True, limit=1)
        if not prices.data:
            return JsonResponse({'error': 'Price not found for the specified product'}, status=404)
        price_id = prices.data[0].id
    except Exception as e:
        logger.error(
            f'Error fetching price for product {product_id}: {str(e)}')
        return JsonResponse({'error': str(e)}, status=500)

    try:
        logger.info(
            'Creating new checkout session for product {}...'.format(product_id))
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    # [price_id, 'price_1OVk2bJQdPkpRk8HOXVcVfEN'],
                    'price': price_id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            automatic_tax={'enabled': True},
            success_url=urljoin(MY_DOMAIN, reverse('shops:payment_success')),
            cancel_url=urljoin(MY_DOMAIN, reverse('shops:payment_cancelled')),
            billing_address_collection='required',
            invoice_creation={'enabled': True,
                              #   'invoice_data': {
                              #         'description': 'purchase a vin report',
                              #         'issuer':'self',
                              #         'footer': 'Thank you for your purchase!',
                              #         }
                              },
            phone_number_collection={"enabled": True},
        )
        if checkout_session.payment_status in ['unpaid', 'incomplete']:
            request.session['checkout_session_id'] = checkout_session.id
            request.session['vin'] = vin
    except Exception as e:
        logger.error(
            f'Error creating checkout session for product {product_id}: {str(e)}')
        return JsonResponse({'error': str(e)}, status=500)

    return redirect(checkout_session.url, code=303)
