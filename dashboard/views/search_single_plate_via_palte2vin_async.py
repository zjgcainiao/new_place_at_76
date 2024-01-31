
from .base import render, fetch_single_plate_data_via_plate2vin_api
from dashboard.forms import LicensePlateSearchForm


async def search_single_plate_via_plate2vin(request):
    form = LicensePlateSearchForm(request.POST or None)
    plate_data = []
    success = False

    if request.method == 'POST':
        if form.is_valid():
            license_plate = form.cleaned_data['license_plate']
            state = form.cleaned_data['state'].upper()

            try:
                plate_data, success = await fetch_single_plate_data_via_plate2vin_api(license_plate, state)
                if not success:
                    form.add_error(
                        None, 'Failed to fetch VIN for the given License Plate.')
            except Exception as e:
                form.add_error(
                    None, f'Error fetching plate data for plate: {license_plate} state:{state} {str(e)}')

    return render(request, 'dashboard/66_vehicle_license_plate_search.html', {'form': form, 'plate_data': plate_data, 'api_success': success})