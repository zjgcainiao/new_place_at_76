from .base import render, redirect,holiday_events
from shift_management.forms import ScheduleShiftForm

def schedule_shift(request):

    form = ScheduleShiftForm()
    if request.method == "POST":
        form = ScheduleShiftForm(request.POST)
        if form.is_valid():
            shift = form.save(commit=False)
            shift.updated_by = request.user
            shift.talent = request.user
            shift.save()
            return redirect('shift_management:schedule_dash')
        
    return render(request,
                  'shift_management/10_schedule_shift.html',
                  {'form': form,
                   'holidays_events': holiday_events
                   })
