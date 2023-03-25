from django.shortcuts import render
from django.urls import reverse_lazy
from homepageapp.models import CustomersNewSQL01Model, VehiclesNewSQL01Model
#, RepairOrdersNewSQL01Model
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, FormView
from django.views.generic.edit import ModelFormMixin
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
# from .serializers import *
from .forms import CustomerModelForm, VehicleModelForm #, RepairOrderModelForm
from django.db.models import Count

def GetHomepageView(request):
    return render(request, 'homepageapp/homepageapp-home.html')


# this is the class-based list view 
class CustomerListView(ListView):
    model = CustomersNewSQL01Model

    context_object_name = 'customers'
    paginate_by = 4  # if pagination is desired
    template_name = 'homepageapp/01-customer-view-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # add a current time into the context.
        context['current_time'] = timezone.now()
        number_of_actives = CustomersNewSQL01Model.objects.annotate(Count('customer_is_activate'))
        context['number_of_actives'] = number_of_actives
        # console.log(f'the context transftered here is {context}' )
        context['form'] = CustomerModelForm()
        # Create any data and add it to the context
        context['addl'] = 'This is just some data'
        return context

    def get_queryset(self):
        return CustomersNewSQL01Model.objects.order_by('-customer_id')

# -------------3/15/2023-------
#GPT 4.0 generated
def customer_list(request):
    customers = CustomersNewSQL01Model.objects.all()
    current_time = timezone.now()
    number_of_actives = CustomersNewSQL01Model.objects.annotate(Count('customer_is_activate'))
    return render(request, 'homepageapp/01-customer-view-list-v2.html', {'customers': customers,
                                                                         'number_of_actives':number_of_actives,
                                                                         'current_time':current_time,})

# -------------------------------

# using the Django formview
# alternative trials --creating a customer model form. then use the formview.
class CustomerModelFormView(FormView):
    emplate_name = 'contact.html'
    form_class = CustomerModelForm()
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # form.send_email()
        return super().form_valid(form)

# createView
class CustomerCreateView(CreateView):
    model = CustomersNewSQL01Model
    fields = ['customer_id', 'customer_first_name','customer_last_name', 'customer_middle_name',
              'customer_does_allow_SMS',]
    template_name = 'homepageapp/02-customer-creation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # add a current time into the context.
        # context['current_time'] = timezone.now()
        # number_of_actives = CustomersNewSQL01Model.objects.annotate(Count('customer_is_activate'))
        # context['number_of_actives'] = number_of_actives
        # console.log(f'the context transftered here is {context}' )
        # context['form'] = CustomerModelForm()
        # Create any data and add it to the context
        context['addl'] = 'This is just some data'
        return context


class CustomerDeleteView(DeleteView):
    model = CustomersNewSQL01Model
    # success_url = reverse_lazy('/')

class CustomerUpdateView(UpdateView):
    model = CustomersNewSQL01Model
    fields = ['customer_id','customer_first_name','customer_last_name', 'customer_middle_name',
              'customer_does_allow_SMS',]
    template_name_suffix = '_updated_form'



# @api_view(['GET', 'POST'])
# def repairorders_list(request):
#     if request.method == 'GET':
#         data = RepairOrdersNewSQL01Model.objects.all()

#         serializer = StudentSerializer(data, context={'request': request}, many=True)

#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = RepairOrderSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['PUT', 'DELETE'])
# def repairorders_detail(request, pk):
#     try:
#         student = Student.objects.get(pk=pk)
#     except Student.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'PUT':
#         serializer = RepairOrderSerializer(student, data=request.data,context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         student.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)