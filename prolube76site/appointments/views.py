from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
# repairOrder model was added on 11/5/2022. Deleted on 11/18/2022
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.views import generic
import os
# Code of your application, which uses environment variables 
# (e.g. from `os.environ` or`os.getenv`) as if they came from the actual one.
from dotenv import load_dotenv

import pymssql
# import pyodbc
import traceback
import sys
import tabulate


def fetch_master_calendar_view(request):
    return render(request, 'appointments/index.html')
    
from django.shortcuts import render, redirect
from .forms import AppointmentRequestForm

def appointment_create_view(request):
    if request.method == 'POST':
        form = AppointmentRequestForm(request.POST)
        if form.is_valid():
            service_request = form.save()
            # TODO: Send email to customer about service request status
            return redirect('service_request_success')
    else:
        form = AppointmentRequestForm()
    return render(request, 'appointments/01-appointment-creation.html', {'form': form})