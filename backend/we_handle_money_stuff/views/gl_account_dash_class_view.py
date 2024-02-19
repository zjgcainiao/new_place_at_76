from .base import ListView
from we_handle_money_stuff.models import GLAccount


class GLAccountDashView(ListView):
    model = GLAccount
    template_name = 'we_handle_money_stuff/30_gl_account_dash.html'
    context_object_name = 'gl_accounts'
    paginate_by = 10
    ordering = ['-id']
    def get_queryset(self):
        return GLAccount.objects.filter(is_active=True)
        # return GLAccount.objects.filter(company=self.request.user.company) # this version can be used with multiple companies (software as a service)