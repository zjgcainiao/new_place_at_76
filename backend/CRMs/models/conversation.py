from .base import models, InternalUser, CustomerUser, uuid
from .operator import Operator
from .ticket import Ticket

class Conversation(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation_name = models.CharField(max_length=128)
    operator = models.ForeignKey(Operator, on_delete=models.DO_NOTHING,
                                 null=True, blank=True,
                                 related_name='conversation_operator')
    tickets = models.ManyToManyField(to=Ticket, blank=True,
                                     related_name='ticket_conversations')

    online = models.ManyToManyField(to=CustomerUser, blank=True,
                                    related_name='customer_users_online')
    logs = models.JSONField(default=list, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_online_count(self):
        return self.online.count()

    def join(self, user):
        self.online.add(user)
        self.save()

    def leave(self, user):
        self.online.remove(user)
        self.save()

    def add_log(self, log):
        if self.logs is None:
            self.logs = []
        self.logs.append(log)
        self.save()

    def __str__(self):
        return f'{self.conversation_name} ({self.get_online_count()})'

