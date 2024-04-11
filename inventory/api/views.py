import json

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


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_my_inventories(request):
    my_inventories = Inventory.objects.filter(user_id=request.user.user_id)

    serializer = InventorySerializer(my_inventories, many=True)
    data = json.loads(json.dumps(serializer.data))

    return Response(data, status=status.HTTP_200_OK)

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
            item = serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if 'expiration_date' in data:
            item.expiration_date = data['expiration_date']

        item.save()

        return Response(f"Item with id {item.item_id} created successfully!", status=status.HTTP_201_CREATED)

    def put(self, args):
        item_id = self.request.data.get('id', None)
        if id is not None:
            try:
                item = InventoryItem.objects.get(item_id=item_id)
            except InventoryItem.DoesNotExist:
                return Response(f"Item with id {item_id} NOT FOUND!", status=status.HTTP_404_NOT_FOUND)

            data = json.loads(json.dumps(self.request.data))
            serializer = InventoryItemSerializer(item, data=data)

            if serializer.is_valid():
                item = serializer.save()
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




@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def shopping_list_view(request):
    # GET to retrieve all shopping lists for the user
    if request.method == 'GET':
        shopping_lists = ShoppingList.objects.filter(user=request.user)
        serializer = ShoppingListSerializer(shopping_lists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # POST to create a new shopping list
    elif request.method == 'POST':
        serializer = ShoppingListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Assuming your ShoppingList model has a 'user' field
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def shopping_list_detail_view(request, list_id):
    # Attempt to retrieve the specified shopping list
    try:
        shopping_list = ShoppingList.objects.get(id=list_id, user=request.user)
    except ShoppingList.DoesNotExist:
        return Response({'error': 'Shopping List not found.'}, status=status.HTTP_404_NOT_FOUND)

    # GET to retrieve a specific shopping list details
    if request.method == 'GET':
        serializer = ShoppingListSerializer(shopping_list)
        return Response(serializer.data)

    # PUT to update a shopping list
    elif request.method == 'PUT':
        serializer = ShoppingListSerializer(shopping_list, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE to remove a shopping list
    elif request.method == 'DELETE':
        shopping_list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)