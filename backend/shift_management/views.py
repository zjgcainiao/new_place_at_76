from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
import holidays
from shift_management.forms import ScheduleShiftForm
from shift_management.models import TimeClock,Shift
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from shift_management.tasks import add_audit_history_record
from core_operations.constants import CURRENT_TIME_SHOW_DATE_WITH_TIMEZONE

us_holidays = holidays.US(years=CURRENT_TIME_SHOW_DATE_WITH_TIMEZONE.year).items()  or {} # Get holidays for current year
holiday_events = [{"title": name, "start": date.isoformat()} for date, name in us_holidays]
holidays_in_json = JsonResponse(holiday_events, safe=False)
def schedule_shift(request):

    form = ScheduleShiftForm()
    if request.method == "POST":
        form = ScheduleShiftForm(request.POST)
        if form.is_valid():
            shift = form.save(commit=False)
            shift.internal_user = request.user
            shift.save()
            return redirect('shift_management:schedule_shift')
        
    return render(request,
                  'shift_management/10_schedule_shift.html',
                  {'form': form,
                   'holidays_events': holiday_events})

def update_shift(request, shift_id):
    shift_instance = Shift.objects.get(id=shift_id)
    content_type = ContentType.objects.get_for_model(shift_instance)
    add_audit_history_record.delay(
        'updated',
        request.user.id,
        f'Shift updated: {shift_instance.id} by {request.user}',
        shift_instance.id,
        content_type,
    )

def clock_in(request):
    if request.method == "POST":
        time_clock = TimeClock(talent=request.user.talentmodel,
                               internal_user=request.user, clock_in_time=timezone.now())
        time_clock.save()
        return redirect('shift_schedule:dashboard')


def clock_out(request):
    if request.method == "POST":
        time_clock = request.user.talentmodel.timeclocks.latest(
            'clock_in')
        time_clock.internal_user = request.user
        time_clock.clock_out_time = timezone.now()
        time_clock.save()
        return redirect('shift_schedule:dashboard')

def shift_dash(request):
    form = ScheduleShiftForm()
    return render(request,
                  'shift_management/20_schedule_dash.html',
                  {'form': form,
                   'us_holidays_json': JsonResponse(events), })