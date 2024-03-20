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

