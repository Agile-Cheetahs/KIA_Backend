from django.db import models

from account.models import Account


class InventoryItem(models.Model):
    item_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    quantity = models.IntegerField()
    UNITS_CHOICES = [
        ('lb', 'lb'),
        ('oz', 'oz'),
        ('g', 'g'),
        ('kg', 'kg'),
        ('count', 'count'),
        ('t', 't'),
    ]
    unit = models.CharField(max_length=10, choices=UNITS_CHOICES)
    LOCATION_CHOICES = [
        ('Pantry', 'Pantry'),
        ('Kitchen', 'Kitchen'),
        ('Cabinet', 'Cabinet'),
    ]
    location = models.CharField(max_length=10, choices=LOCATION_CHOICES)
    expiration_date = models.DateField(null=True, blank=True)
    CATEGORY_CHOICES = [
        ('Fruit', 'Fruit'),
        ('Grocery', 'Grocery'),
    ]
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f"{self.name} - {self.quantity} {self.unit}"


class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Account, related_name='inventory', on_delete=models.CASCADE)
    items = models.ManyToManyField(InventoryItem, related_name='items', blank=True)

    class Meta:
        verbose_name_plural = "Inventories"

    def __str__(self):
        return f"Inventory for {self.user.__str__()}"
