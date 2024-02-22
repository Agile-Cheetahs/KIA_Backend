from rest_framework import serializers
from account.models import *


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password', 'role']

    def save(self):
        role = ''
        if 'role' not in self.validated_data:
            role = 'normal-user'

        account = Account(
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            phone_number=self.validated_data['phone_number'],
            role=role,
        )
        password = self.validated_data['password']

        account.set_password(password)
        account.save()
        return account


class AccountPropertiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number',
                  'gender', 'image', 'role', 'bio', 'birthday']
