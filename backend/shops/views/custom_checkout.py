
from .base import render,settings,reverse

def custom_checkout(request, product_id):
    """
    Renders the custom checkout page for the specified product.
    """
    return_url = request.build_absolute_uri(reverse('shops:payment_success'))

    return render(request, 'shops/21_custom_checkout.html',{
        
        'product_id': product_id,
        'GOOGLE_MAP_API_KEY': settings.GOOGLE_MAP_API_KEY,
        'return_url': return_url,
        'stripe_public_key': settings.STRIPE_PUBLIC_LIVE_KEY 
                    if (not settings.DEBUG) and settings.DJANGO_PROD_ENV==True
                    else settings.STRIPE_PUBLIC_TEST_KEY,
        })
