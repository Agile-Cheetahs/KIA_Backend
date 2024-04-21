import json

from django.db import transaction
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from inventory.api.serializer import *
from inventory.models import *


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_all_inventories(request):
    if request.user.role == 'superuser':
        all_inventories = Inventory.objects.all()

        serializer = InventorySerializer(all_inventories, many=True)
        data = json.loads(json.dumps(serializer.data))

        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response("ERROR: You are not permitted to make this request!", status=status.HTTP_403_FORBIDDEN)


@permission_classes((IsAuthenticated,))
class MyInventory(APIView):
    def get(self, args):
        my_inventories = Inventory.objects.filter(user_id=self.request.user.user_id)

        serializer = InventorySerializer(my_inventories, many=True)
        data = json.loads(json.dumps(serializer.data))

        return Response(data, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, args):
        data = json.loads(json.dumps(self.request.data))
        serializer = InventorySerializer(data=data)

        if serializer.is_valid():
            if Inventory.objects.filter(user_id=self.request.user.user_id).exists():
                return Response("ERROR: This user has created an inventory before! "
                                "Every user should have at most one inventory.",
                                status=status.HTTP_403_FORBIDDEN)
            else:
                data = serializer.validated_data
                data['user'] = self.request.user

                inventory = serializer.create(validated_data=data)
                inventory.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(f"Inventory with id {inventory.inventory_id} created successfully!",
                        status=status.HTTP_201_CREATED)


@permission_classes((IsAuthenticated,))
class InventoryItemCRUD(APIView):
    def get(self, args):
        item_id = self.request.query_params.get('id', None)
        if item_id is not None:
            try:
                item = InventoryItem.objects.get(item_id=item_id)
            except InventoryItem.DoesNotExist:
                return Response(f"Item with id {item_id} NOT FOUND!", status=status.HTTP_404_NOT_FOUND)

            serializer = InventoryItemSerializer(item)
            data = json.loads(json.dumps(serializer.data))

            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response("Id: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)

    def post(self, args):
        data = json.loads(json.dumps(self.request.data))
        serializer = InventoryItemSerializer(data=data)

        if serializer.is_valid():
            if 'location' in data:
                location, created = Location.objects.get_or_create(name=data['location'])
            else:
                location, created = Location.objects.get_or_create(name='Kitchen')

            item = serializer.save(location=location)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if 'expiration_date' in data:
            item.expiration_date = data['expiration_date']

        item.save()

        return Response(f"Item with id {item.item_id} created successfully!", status=status.HTTP_201_CREATED)

    def put(self, args):
        item_id = self.request.query_params.get('id', None)
        if id is not None:
            try:
                item = InventoryItem.objects.get(item_id=item_id)
            except InventoryItem.DoesNotExist:
                return Response(f"Item with id {item_id} NOT FOUND!", status=status.HTTP_404_NOT_FOUND)

            data = json.loads(json.dumps(self.request.data))
            serializer = InventoryItemSerializer(item, data=data)

            if serializer.is_valid():
                if 'location' in data:
                    location, created = Location.objects.get_or_create(name=data['location'])
                else:
                    location, created = Location.objects.get_or_create(name='Kitchen')

                item = serializer.save(location=location)

                if 'expiration_date' in data:
                    item.expiration_date = data['expiration_date']

                item.save()
                return Response({'message': f"Item with id {item.item_id} updated successfully!",
                                 'data': json.loads(json.dumps(serializer.data))}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Id: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, args):
        item_id = self.request.query_params.get('id', None)
        if item_id is not None:
            try:
                item = InventoryItem.objects.get(item_id=int(item_id))
                item.delete()
                return Response(f"Item with id {item_id} removed successfully!",
                                status=status.HTTP_204_NO_CONTENT)
            except InventoryItem.DoesNotExist:
                return Response(f"Item with id {item_id} NOT FOUND!", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("Id: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticated,))
class LocationCRUD(APIView):
    def get(self, args):
        loc_id = self.request.query_params.get('id', None)
        if loc_id is not None:
            try:
                location = Location.objects.get(location_id=loc_id)
            except Location.DoesNotExist:
                return Response(f"Item with id {loc_id} NOT FOUND!", status=status.HTTP_404_NOT_FOUND)

            serializer = LocationSerializer(location)
        else:
            try:
                my_inventory = Inventory.objects.get(user=self.request.user)
            except Inventory.DoesNotExist:
                return Response(f"No inventory found for this user!", status=status.HTTP_404_NOT_FOUND)

            locations = list(item.location for item in my_inventory.items.all())
            serializer = LocationSerializer(locations, many=True)

        data = json.loads(json.dumps(serializer.data))
        return Response(data, status=status.HTTP_200_OK)

    def post(self, args):
        data = json.loads(json.dumps(self.request.data))
        serializer = LocationSerializer(data=data)

        if serializer.is_valid():
            location = serializer.save()
            self.request.user.locations.add(location)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(f"Location with id {location.location_id} created successfully!", status=status.HTTP_201_CREATED)

    def put(self, args):
        loc_id = self.request.query_params.get('id', None)
        if loc_id is not None:
            try:
                location = Location.objects.get(location_id=loc_id)
            except Location.DoesNotExist:
                return Response(f"Location with id {loc_id} NOT FOUND!", status=status.HTTP_404_NOT_FOUND)

            data = json.loads(json.dumps(self.request.data))
            serializer = LocationSerializer(location, data=data)

            if serializer.is_valid():
                location = serializer.save()
                return Response({'message': f"Location with id {location.location_id} updated successfully!",
                                 'data': json.loads(json.dumps(serializer.data))}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Id: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, args):
        loc_id = self.request.query_params.get('id', None)
        if loc_id is not None:
            try:
                location = Location.objects.get(location_id=loc_id)
                location.delete()
                self.request.user.locations.remove(location)
                return Response(f"Location with id {loc_id} removed successfully!",
                                status=status.HTTP_204_NO_CONTENT)
            except Location.DoesNotExist:
                return Response(f"Location with id {loc_id} NOT FOUND!", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("Id: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def shopping_list(request):
    if request.method == 'GET':
        lists = ShoppingList.objects.filter(user=request.user)
        serializer = ShoppingListSerializer(lists, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ShoppingListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def shopping_list_detail(request, pk):
    list_ = get_object_or_404(ShoppingList, pk=pk, user=request.user)
    if request.method == 'GET':
        serializer = ShoppingListSerializer(list_)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ShoppingListSerializer(list_, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        list_.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_item_to_shopping_list(request, list_pk):
    # Get the shopping list object
    list_ = get_object_or_404(ShoppingList, pk=list_pk, user=request.user)
    
    # Create a new item
    serializer = ShoppingListItemSerializer(data=request.data)
    if serializer.is_valid():
        item = serializer.save()
        # Add the new item to the shopping list
        list_.items.add(item)
        list_.save()  # Make sure to save the list object to update the database
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def modify_or_remove_item_from_list(request, list_pk, item_pk):
    list_ = get_object_or_404(ShoppingList, pk=list_pk, user=request.user)
    item = get_object_or_404(ShoppingListItem, pk=item_pk)

    if request.method == 'PUT':
        serializer = ShoppingListItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        list_.items.remove(item)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
