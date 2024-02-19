from django import db
from .base import models, settings
from customer_users.models import CustomerUser
class Cart(models.Model):
    id = models.BigAutoField(primary_key=True)
    customer_user = models.OneToOneField(CustomerUser, on_delete=models.CASCADE, related_name='cart')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cart'
        ordering = ('-created_at',)


    def __str__(self):
        return f'Cart for {self.user}'