from .base import UpdateView, LoginRequiredMixin, redirect, messages, \
    render, reverse_lazy, timezone, logger
from dashboard.forms import PersonalItemUpdateForm
from homepageapp.models import MovingItem, MovingRequest
from dashboard.forms import MovingItemForm
from django.core.exceptions import ObjectDoesNotExist
from core_operations.utilities import generate_code128_barcode_lite


def moving_item_update(request):
    if request.method == 'POST':
        form = MovingItemForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page or list
            return redirect('dashboard:moving_item_dash')
    else:
        form = MovingItemForm()
    return render(request, 'dashboard/113_moving_request_update.html', {'form': form})
