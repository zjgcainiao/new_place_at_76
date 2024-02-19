from .base import ListView
from we_handle_money_stuff.models import GLSubAccount


class GLSubAccountDashView(ListView):
    model = GLSubAccount
    template_name = 'we_handle_money_stuff/20_gl_sub_account_dash.html'
    context_object_name = 'gl_sub_accounts'
    paginate_by = 10
    ordering = ['-id']
    
    def get_queryset(self):
        return GLSubAccount.objects.filter(is_active=True)
        # return GLAccount.objects.filter(company=self.request.user.company) # this version can be used with multiple companies (software as a service)