
from .base import render, redirect, login_required,messages, logger
from we_handle_money_stuff.models import GLSubAccount



@login_required(login_url='internal_users:int_user_login')
def gl_sub_account_detail(request, pk):
    gl_sub_account = GLSubAccount.objects.get(pk=pk)
    if gl_sub_account:
        return render(request, 'we_handle_money_stuff/21_gl_sub_account_detail.html', {'gl_sub_account': gl_sub_account})
    else:
        messages.error(request, 'GL Account {pk} not found')
        logger.error(f'GL Account {pk} not found')
        return redirect('we_handle_money_stuff:gl_sub_account_dash')
