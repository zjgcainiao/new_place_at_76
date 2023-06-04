from django.shortcuts import render

# Create your views here.
def engine_model_view(request):
    return render(request, 'we_create_3d_models/10_sample.html')