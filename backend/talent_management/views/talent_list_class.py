from .base import TalentsModel, InternalUserRequiredMixin, reverse_lazy, ListView, Q, re, \
                 messages, render, InternalUser

class TalentListView(InternalUserRequiredMixin, ListView):
    model = TalentsModel
    context_object_name = 'talent_list'
    template_name = 'talent_management/10_talent_list.html'
    login_url = reverse_lazy('internal_users:internal_user_login')

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            talent_is_active=True).order_by('-talent_id')
        # queryset = queryset
        # Check if search query is provided
        # the search bar's name in the html template is 'talent-search-query'
        search_query = self.request.GET.get('q')  # 'talent-search-query'

        # search_keywords = self.request.GET.get('talent_first_name'), self.request.GET.get('talent_last_name'), self.request.GET.get('talent_email')
        if search_query:
            # Retrieve search query by ID
            # search_query_by_id = self.request.GET.get('talent-search')

            queryset = queryset.filter(
                Q(talent_first_name__icontains=search_query) |
                Q(talent_last_name__icontains=search_query) |
                Q(talent_email__icontains=search_query) |
                Q(talent_phone_number_primary__icontains=search_query)
            )
            # Remove non-digit characters from the search query
            search_query_digits = re.sub(r'\D', '', search_query)
            # and re.match(r'^\d+$', search_query):
            if len(search_query_digits) == 10:
                # Format the search query as per the phone number pattern
                search_query_digits = "1" + search_query_digits
                formatted_search_query = '+{}({}){}-{}'.format(
                    search_query_digits[0:1],
                    search_query_digits[1:4],
                    search_query_digits[4:7],
                    search_query_digits[7:11],
                )
                queryset = queryset.filter(
                    talent_phone_number_primary__icontains=formatted_search_query)
            elif len(search_query_digits) == 11:
                formatted_search_query = '+{}({}){}-{}'.format(
                    search_query_digits[0:1],
                    search_query_digits[1:4],
                    search_query_digits[4:7],
                    search_query_digits[7:11],
                )
                queryset = queryset.filter(
                    Q(talent_phone_number_primary__icontains=formatted_search_query))
        return queryset

    def dispatch(self, request, *args, **kwargs):
        # user has to be instance of InternalUser.
        if isinstance(request.user, InternalUser):
            if not (request.user.is_authenticated):
                messages.error(
                    request, "You do not have permission to access this page.")
                return render(request, 'talent_management/30_user_has_no_permission.html')
            # Check if the user has the required user_auth_group
            # this field shall be strictly controlled and logged. CFO and CTO approvals are required.
            if not hasattr(request.user, 'user_auth_group') or request.user.user_auth_group != 3 :
                messages.error(
                    request, "You do not have permission to access this page.")
                return render(request, 'talent_management/30_user_has_no_permission.html')
        else:
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)