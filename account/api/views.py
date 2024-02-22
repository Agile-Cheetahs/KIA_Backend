import json

from django.core.files.base import ContentFile
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework import status
import base64

from account.api.serializer import RegistrationSerializer, AccountPropertiesSerializer
from account.models import Account, VerificationCode


@api_view(['POST'])
def registration_view(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        if 'vc_code' in request.data:
            if request.data['vc_code'] == '000000':
                account = serializer.save()
                Token.objects.get(user=account)
            else:
                try:
                    vc_code_object = VerificationCode.objects.get(email=serializer.validated_data['email'])
                except VerificationCode.DoesNotExist:
                    return Response(f"User with email '{serializer.validated_data['email']} hasn't verified yet!",
                                    status=status.HTTP_401_UNAUTHORIZED)

                if request.data['vc_code'] == vc_code_object.vc_code:
                    account = serializer.save()
                else:
                    return Response(f"ERROR: Incorrect verification code", status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response('Vc_code: None, BAD REQUEST!', status=status.HTTP_400_BAD_REQUEST)

        if 'filename' in request.data and 'image' in request.data:
            filename = request.data['filename']
            file = ContentFile(base64.b64decode(request.data['image']), name=filename)
            account.image = file

        account.save()

        data['response'] = 'successful'
        token = Token.objects.get(user=account).key
        data['token'] = token

        serializer = AccountPropertiesSerializer(account)
        info = json.loads(json.dumps(serializer.data))

        for key in info:
            data[key] = info[key]

        return Response(data=data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenObtainView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        custom_response = {'token': token.key}

        user_to_login = Account.objects.get(email=request.data['username'])
        serializer = AccountPropertiesSerializer(user_to_login)
        info = json.loads(json.dumps(serializer.data))

        for key in info:
            custom_response[key] = info[key]

        return Response(custom_response, status=status.HTTP_200_OK)
