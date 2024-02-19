
from .base import render, redirect, login_required,messages, logger
from we_handle_money_stuff.models import GLAccount



@login_required(login_url='internal_users:int_user_login')
def gl_account_soft_delete(request,pk):
    gl_account = GLAccount.objects.get(pk=pk)
    gl_account.is_active = False
    gl_account.save()
    messages.success(request, 'GL Account has been soft deleted. ')
    logger.info(f'GL Account {gl_account} soft deleted by {request.user}')
    return redirect('we_handle_money_stuff:gl_account_dash')