from django.db import models

# Create your models here.


class OnlineProducts(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True,
                            blank=True, verbose_name="Product Name")
    delivery_method = models.CharField(max_length=20, null=True, blank=True)
