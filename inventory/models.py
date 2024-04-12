from django.db import models

from account.models import Account


from django.db.models.signals import pre_delete


class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


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
    units = models.CharField(max_length=10, choices=UNITS_CHOICES)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    expiration_date = models.DateField(null=True, blank=True)
    CATEGORY_CHOICES = [
        ('Fruit', 'Fruit'),
        ('Grocery', 'Grocery'),
    ]
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f"{self.name} - {self.quantity} {self.units}"


class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(Account, related_name='inventory', on_delete=models.CASCADE)
    items = models.ManyToManyField(InventoryItem, related_name='inventories')

    class Meta:
        verbose_name_plural = "Inventories"

    def __str__(self):
        return f"Inventory for {self.user.__str__()}"


def delete_inventory(sender, instance, **kwargs):
    for item in instance.items.all():
        item.delete()


pre_delete.connect(delete_inventory, sender=Inventory)


# shopping list table
class ShoppingListItem(models.Model):
    item_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    units = models.CharField(max_length=10)  
    crossed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.quantity} {self.units} - {'Crossed' if self.crossed else 'Not Crossed'}"


def get_default_user():
    # Returns the user_id of the first user. You might want to handle the case when there are no users.
    first_user = Account.objects.first()
    return first_user.user_id if first_user else None


class ShoppingList(models.Model):
    list_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    items = models.ManyToManyField(ShoppingListItem, related_name='shopping_items', blank=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='shopping_lists', default=get_default_user)
    is_favorite = models.BooleanField(default=False)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {'Favorite' if self.is_favorite else 'Regular'} List"
