from rest_framework import serializers, status
from rest_framework.response import Response

from account.api.serializer import AccountPropertiesSerializer
from inventory.models import *


class InventoryItemSerializer(serializers.ModelSerializer):
    expiration_date = serializers.DateField(required=False)

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
                    new_item = item_serializer.save()

                    if 'expiration_date' in item_data:
                        new_item.expiration_date = item_data['expiration_date']

                    new_item.save()
                    new_items.append(new_item)
                else:
                    return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("BAD REQUEST: items", status=status.HTTP_400_BAD_REQUEST)

        inventory = Inventory.objects.create(user=validated_data['user'])
        inventory.items.set(new_items)

        return inventory
