from django.urls import path
from we_handle_money_stuff.views import GLAccountDashView,gl_account_create,gl_account_update, \
        gl_account_soft_delete,gl_account_delete, gl_account_detail, \
        GLSubAccountDashView, gl_sub_account_create, gl_sub_account_update, \
        gl_sub_account_soft_delete, gl_sub_account_delete, gl_sub_account_detail 

app_name = "we_handle_money_stuff"

urlpatterns = [
    path('gl-accounts/', GLAccountDashView.as_view(), name='gl_account_dash'),
    path('gl-accounts/create/', gl_account_create, name='gl_account_create'),
    path('gl-accounts/<int:pk>/detail/', gl_account_detail, name='gl_account_detail'),
    path('gl-accounts/<int:pk>/update/', gl_account_update, name='gl_account_update'),
    path('gl-accounts/<int:pk>/soft-delete/', gl_account_soft_delete, name='gl_account_soft_delete'),
    path('gl-accounts/<int:pk>/delete/', gl_account_delete, name='gl_account_delete'),


    path('gl-sub-accounts/', GLSubAccountDashView.as_view(), name='gl_sub_account_dash'),
    path('gl-sub-accounts/create/', gl_sub_account_create, name='gl_sub_account_create'),
    path('gl-sub-accounts/<int:pk>/detail/', gl_sub_account_detail, name='gl_sub_account_detail'),
    path('gl-sub-ccounts/<int:pk>/update/', gl_sub_account_update, name='gl_sub_account_update'),
    path('gl-sub-accounts/<int:pk>/soft-delete/', gl_sub_account_soft_delete, name='gl_sub_account_soft_delete'),
    path('gl-sub-accounts/<int:pk>/delete/', gl_sub_account_delete, name='gl_sub_account_delete'),
# path('gl-journal-entries/', views.GLJournalEntryListCreateView.as_view(), name='gl-journal-entries-list-create'),
]
