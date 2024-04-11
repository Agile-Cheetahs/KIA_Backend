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


class ShoppingListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingListItem
        fields = '__all__'

class ShoppingListSerializer(serializers.ModelSerializer):
    items = ShoppingListItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = ShoppingList
        fields = ['list_id', 'name', 'items', 'is_favorite', 'is_complete']
