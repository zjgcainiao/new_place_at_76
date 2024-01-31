from homepageapp.models import TextMessagesModel
from .base import render

def chat_sidebar_view(request, customer_id):
    text_messages = TextMessagesModel.objects.filter(
        text_customer=customer_id).order_by('-text_message_id')[:10]
    context = {
        'text_messages': text_messages,
        # 2023-04-18: in dashboard_detail_v1() function, there stores a `customer_id` in the request.session ensures persistence in data.
        # hence i am planning to not include this variable in the context
        'customer_id': customer_id,
    }
    return render(request, 'dashboard/50_text_message_side_bar.html', context)
