from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from account.models import Account
# Create your models here.


class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    units = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    expiration = models.DateField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class Inventory(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    items = models.ManyToManyField(InventoryItem)

    def __str__(self):
        return f"{self.user.name}'s Inventory"