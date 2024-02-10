from .base import View, render, InternalUserRequiredMixin, reverse, sync_to_async, Prefetch,re,logger,Q
from dashboard.forms import SearchForm
from homepageapp.models import RepairOrdersNewSQL02Model,PaymentsModel
from appointments.models import AppointmentRequest

# added on 2023-06-03. ChatGPT generated.
# search form page --- the first step before creating an repair order.
class SearchView(View, InternalUserRequiredMixin):

    # login_url = reverse_lazy('internal_users:internal_user_login')
    def _parse_phone_number(self, phone_str):
        """Extracts digits from common phone number formats."""
        return re.sub(r'\D', '', phone_str)
    
    async def get(self, request):
        form = SearchForm()
        context = {'appointments': None,
                   'repair_orders': None,
                   'form': form,  # re-render the form with its data.
                   }
        return render(request, 'dashboard/30_search.html', {'form': form})

    async def post(self, request):
        form = SearchForm(request.POST)

        if form.is_valid():

            search_query = form.cleaned_data['search_query']
           # Check if search_query looks like a phone number
            if re.search(r'\d', search_query):
                search_query = self._parse_phone_number(search_query)
            # using sync_to_async to wrap around a search query processing in both appointments and repairorders models.
            appointments = await sync_to_async(self._get_appointments, thread_sensitive=True)(search_query)
            repair_orders = await sync_to_async(self._get_active_repair_orders, thread_sensitive=True)(search_query)
            # Perform the search query in the appointments or other relevant models
            # appointments = AppointmentRequest.objects.filter(Q(appointment_phone_number__icontains=search_query) |
            #                                                  Q(appointment_email__icontains=search_query)).order_by('appointment_id')

            # repair_orders = RepairOrdersNewSQL02Model.objects.prefetch_related(
            #     Prefetch('repair_order_customer__addresses')).prefetch_related(
            #     'repair_order_customer__phones').prefetch_related('repair_order_customer__emails'
            #                                                       )

            # repair_orders = repair_orders.filter(
            #     repair_order_customer__emails__email_address__icontains=search_query
            # ).filter(repair_order_customer__phones__phone_number__icontains=search_query)

            context = {'appointments': appointments,
                       'repair_orders': repair_orders,
                       'form': form,  # re-render the form with its data.
                       }

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':

                return render(request, 'dashboard/31_search_results.html', context)
            else:
                print('using 30_search.html')
                return render(request, 'dashboard/30_search.html', context)
            # if appointments.exists():
            #     return render(request, 'dashboard/20_search.html', {'appointments': appointments})
            # else:
            #     return render(request, 'dashboard/20_search.html', {'no_match': True})
        else:
            return render(request, 'dashboard/30_search.html', {'form': form})

    def _get_appointments(self, search_query):
        return list(AppointmentRequest.objects.filter(
            Q(appointment_phone_number__icontains=search_query) |
            Q(appointment_phone_number_digits_only__icontains=search_query) |
            Q(appointment_email__icontains=search_query)
        ).order_by('-appointment_id'))

    def _get_active_repair_orders(self, search_query):
        logger.info('search any matched repair order records before creating one...')

        # Prefetch payment information related to each repair order to the attribute of "payments"
        payment_prefetch = Prefetch(
            'payment_repairorders',
            queryset=PaymentsModel.objects.all(),
            to_attr='payments'
        )
        queryset = RepairOrdersNewSQL02Model.objects.prefetch_related(
            'repair_order_customer',
            'repair_order_phase',
            'repair_order_vehicle',
            'repair_order_vehicle__vehiclenotes_vehicle',
            'repair_order_customer__taxes',
            'repair_order_customer__addresses',
            'repair_order_customer__phones',
            'repair_order_customer__emails',
            payment_prefetch,
            # filtering out only active repair orders
        ).filter(
            repair_order_phase__gte=1,
            repair_order_phase__lte=5
        ).filter(
            Q(repair_order_customer__emails__email_address__icontains=search_query) |
            Q(repair_order_customer__phones__phone_number__icontains=search_query) |
            Q(repair_order_customer__phones__phone_number_digits_only__icontains=search_query) 
        )
        # Execute the query and return the results
        # repair_orders = await database_sync_to_async(list)(queryset)

        # .filter() calls in Django ORM does not get executed unless the queryset is evaluated.
        # when calling list() on the queset, the sql server executes the script
        return list(queryset)