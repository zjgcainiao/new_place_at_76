from .base import models

from .cart import Cart
from .online_product import OnlineProducts

class CartItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING, related_name='items')
    product = models.ForeignKey(OnlineProducts, on_delete=models.DO_NOTHING,
                                related_name = 'cart_items'
                                )  # Assuming you have a Product model
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cart_items'
        ordering = ('-added_at',)
        unique_together = ('cart', 'product')