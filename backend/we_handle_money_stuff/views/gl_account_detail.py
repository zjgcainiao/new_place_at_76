
from .base import render, redirect, login_required,messages, logger
from we_handle_money_stuff.models import GLAccount



@login_required(login_url='internal_users:int_user_login')
def gl_account_detail(request, pk):
    gl_account = GLAccount.objects.get(pk=pk)
    if gl_account:
        return render(request, 'we_handle_money_stuff/31_gl_account_detail.html', {'gl_account': gl_account})
    else:
        messages.error(request, 'GL Account {pk} not found')
        logger.error(f'GL Account {pk} not found')
        return redirect('we_handle_money_stuff:gl_account_dash')
