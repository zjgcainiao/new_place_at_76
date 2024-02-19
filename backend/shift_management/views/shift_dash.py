from .base import render, holiday_events, JsonResponse
from shift_management.forms import ScheduleShiftForm
from shift_management.models import Shift



def shift_dash(request):
    # form = ScheduleShiftForm()
    shifts = Shift.objects.prefetch_related('shift_work_sessions').all()
    context = {
                    'shifts': shifts,
                    #   'form': form,
                   'us_holidays_json': JsonResponse(holiday_events,safe=False), 
                   'holidays_events': holiday_events}
    
    return render(request,
                  'shift_management/20_shift_dash.html',
                  context= context
                 )