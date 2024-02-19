
from .base import render, redirect, login_required,messages, logger
from we_handle_money_stuff.models import GLAccount



@login_required(login_url='internal_users:int_user_login')
def gl_account_delete(request,pk):
    gl_account = GLAccount.objects.get(pk=pk)
    gl_account.delete()
    messages.success(request, 'GL Account Deleted')
    logger.info(f'GL Account {gl_account} deleted by {request.user}')
    return redirect('we_handle_money_stuff:gl_account_dash')