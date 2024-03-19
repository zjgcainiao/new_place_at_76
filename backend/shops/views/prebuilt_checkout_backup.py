from django.http import HttpResponseRedirect
from django.urls import reverse


def prebuilt_checkout_backup(request, vin):
    """
    Redirects old URL pattern /shops/prebuilt/<vin> to the new pattern /shops/prebuilt-checkout/?vin=<vin>.
    """
    redirect_url = reverse('shops:prebuilt_checkout') + f'?vin={vin}'
    return HttpResponseRedirect(redirect_url)
