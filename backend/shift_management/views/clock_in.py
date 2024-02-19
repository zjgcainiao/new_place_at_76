from shift_management.models import  WorkSession,Shift
from .base import redirect, timezone


def clock_in(request,pk):
    if request.method == "POST":
        work_session = WorkSession(talent=request.user.user_talent,
                                   shift= Shift.objects.get(pk=pk),
                               clock_in_time=timezone.now())
        work_session.save()
        return redirect('shift_managment:shift_dash')