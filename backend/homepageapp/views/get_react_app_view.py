

from .base import TemplateView, reverse_lazy


class GetReactAppView(TemplateView):
    template_name = 'homepageapp/13_react_app_portal.html'
    login_url = reverse_lazy('internal_users:internal_user_login')
