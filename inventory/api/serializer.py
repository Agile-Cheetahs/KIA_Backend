from rest_framework import serializers

from account.api.serializer import AccountPropertiesSerializer
from inventory.models import *


class InventoryItemSerializer(serializers.ModelSerializer):
    expiration_date = serializers.DateField(required=False)
    location = serializers.CharField(required=False)

    class Meta:
        model = InventoryItem
        fields = '__all__'


class InventorySerializer(serializers.ModelSerializer):
    user = AccountPropertiesSerializer(read_only=True)
    items = InventoryItemSerializer(many=True)

    class Meta:
        model = Inventory
        fields = '__all__'

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])

        try:
            new_items = []
            for item_data in items_data:
                item_serializer = InventoryItemSerializer(data=item_data)
                if item_serializer.is_valid():
                    if 'location' in item_data:
                        location, created = Location.objects.get_or_create(name=item_data['location'])
                    else:
                        location, created = Location.objects.get_or_create(name='Kitchen')

                    new_item = item_serializer.save(location=location)

                    if 'expiration_date' in item_data:
                        new_item.expiration_date = item_data['expiration_date']

                    new_item.save()
                    new_items.append(new_item)
                else:
                    raise Exception(item_serializer.errors)
        except:
            raise Exception("BAD REQUEST: items")

        inventory = Inventory.objects.create(user=validated_data['user'])
        inventory.items.set(new_items)

        return inventory


class LocationSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Location
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
