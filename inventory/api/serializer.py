from rest_framework import serializers

from account.api.serializer import AccountPropertiesSerializer
from inventory.models import *


class InventoryItemSerializer(serializers.ModelSerializer):
    expiration_date = serializers.DateField(required=False)

    class Meta:
        model = InventoryItem
        fields = '__all__'


class InventorySerializer(serializers.ModelSerializer):
    user = AccountPropertiesSerializer(read_only=True)
    items = InventoryItemSerializer(many=True, read_only=True)

    class Meta:
        model = Inventory
        fields = '__all__'
