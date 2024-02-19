from .base import redirect, timezone
from shift_management.models import  WorkSession,Shift

def clock_out(request,pk):
    if request.method == "POST":
        work_session = request.user.user_talent.timeclocks.latest(
            'clock_in')
        work_session.internal_user = request.user
        work_session.clock_out = timezone.now()
        work_session.save()
        return redirect('shift_managment:shift_dash')