from django.urls import reverse_lazy,reverse
from django.views.generic.edit import DeleteView
from homepageapp.models import LineItemsNewSQL02Model

class LineItemDeleteView(DeleteView):
    model = LineItemsNewSQL02Model
    template_name = 'dashboard/99_line_item_delete_view.html'  # DeleteView template
    
    # No need to override get_queryset unless you have specific restrictions
    
    def get_success_url(self):
        # Get the RepairOrder's pk from the URL
        repair_order_pk = self.kwargs.get('pk')
        # Redirect to the RepairOrder detail view
        return reverse('dashboard:get_wip_detail_v1', kwargs={'pk': repair_order_pk})
    
    def get_queryset(self):
        """Ensure that only line items that the user is allowed to delete are queried."""
        # Customize this method based on your user permissions.
        return super().get_queryset()