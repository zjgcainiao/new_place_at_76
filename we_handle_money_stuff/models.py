from django.db import models


class Vendor(models.Model):
    name = models.CharField(max_length=255)


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class PurchaseOrder(models.Model):
    order_date = models.DateTimeField()
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    description = models.TextField()


class PurchaseInvoice(models.Model):
    invoice_number = models.AutoField(primary_key=True)
    invoice_date = models.DateTimeField()
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    description = models.TextField()


class InvoiceLine(models.Model):
    invoice = models.ForeignKey(PurchaseInvoice, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)


class Journal(models.Model):
    name = models.CharField(max_length=255)


class Account(models.Model):
    name = models.CharField(max_length=255)
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)


class SubAccount(models.Model):
    name = models.CharField(max_length=255)
    parent_account = models.ForeignKey(Account, on_delete=models.CASCADE)


class JournalEntry(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    sub_account = models.ForeignKey(
        SubAccount, on_delete=models.CASCADE, null=True, blank=True)
    debit = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    credit = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    date = models.DateTimeField()
    description = models.TextField()
