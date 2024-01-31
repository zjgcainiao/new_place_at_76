from .base import JsonResponse, timezone
from homepageapp.models import VehiclesNewSQL02Model

def update_customer_assignment(request):
    if request.method == 'POST':
        vehicle_id = request.POST.get('vehicleId')
        selected_customer = request.POST.get('selectedCustomer')

        try:
            vehicle = VehiclesNewSQL02Model.objects.get(id=vehicle_id)
            vehicle.vehicle_cust = selected_customer
            vehicle.vehicle_last_updated_at = timezone.now()
            vehicle.modified_by = request.user  # assuming the user is logged in
            vehicle.save()
            return JsonResponse({'status': 'success', 'message': 'Customer assignment updated successfully.'})
        except VehiclesNewSQL02Model.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Vehicle not found.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})