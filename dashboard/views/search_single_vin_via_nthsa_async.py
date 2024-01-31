from .base import render, logger, fetch_and_save_single_vin_from_nhtsa_api
from dashboard.forms import VINSearchForm

async def search_single_vin_via_nhtsa(request):
    vin_data_list = []
    count = 0

    if request.method == 'POST':
        form = VINSearchForm(request.POST)
        if form.is_valid():
            vin = form.cleaned_data['vin']
            year = form.cleaned_data['year']

            logger.info(
                f'performing a manual single vin search on webpage for vin {vin} and model year {year}...')

            vin_data_list, number_of_downgraded_records, created = await fetch_and_save_single_vin_from_nhtsa_api(vin, year)
    else:
        form = VINSearchForm()

    if vin_data_list:
        count = vin_data_list[0].results_count
    else:
        count = None

    context = {
        'form': form,
        'vin_data_list': vin_data_list,
        'count': count
    }
    return render(request, 'dashboard/65_vehicle_vin_search.html', context)
