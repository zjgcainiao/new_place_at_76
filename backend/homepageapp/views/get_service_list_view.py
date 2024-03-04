from .base import render


def GetServiceListView(request):
    return render(request, 'homepageapp/21_homepageapp_service_list.html')
