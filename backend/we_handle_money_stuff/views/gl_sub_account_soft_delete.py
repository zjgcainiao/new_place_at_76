
from .base import render, redirect, login_required,messages, logger
from we_handle_money_stuff.models import GLSubAccount

@login_required(login_url='internal_users:int_user_login')
def gl_sub_account_soft_delete(request,pk):
    gl_sub_account = GLSubAccount.objects.get(pk=pk)
    gl_sub_account.is_active = False
    gl_sub_account.save()
    messages.success(request, 'GL Sub Account deleted.')
    logger.info(f'GL Sub Account {gl_sub_account} deleted by {request.user}.')
    return redirect('we_handle_money_stuff:gl_sub_account_dash')