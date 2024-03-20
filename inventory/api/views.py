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

