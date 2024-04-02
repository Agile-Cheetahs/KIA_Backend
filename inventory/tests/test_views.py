import os
import json

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.conf import settings
import tempfile
from datetime import datetime, timedelta

from inventory.models import *
from account.models import Account

client = Client()


class CheckGetAllInventories(TestCase):
    """ Test module for get the whole inventories for all users """

    def setUp(self):
        new_user = Account.objects.create(
            first_name='Danial',
            last_name='Bazmandeh',
            email='danibazi9@gmail.com',
            phone_number='+989152147655',
            gender='Male',
            password='123456'
        )

        superuser = Account.objects.create(
            first_name='admin',
            last_name='admin',
            email='admin@admin.com',
            phone_number='10000003243',
            password='123456',
            role='superuser'
        )

        new_item_1 = InventoryItem.objects.create(
            name='Test Item 1',
            quantity=5,
            unit='lb',
            location='Kitchen',
            category='Fruit'
        )

        new_item_2 = InventoryItem.objects.create(
            name='Test Item 2',
            quantity=10,
            unit='kg',
            location='Pantry',
            category='Fruit'
        )

        new_item_3 = InventoryItem.objects.create(
            name='Test Item 3',
            quantity=100,
            unit='kg',
            location='Cabinet',
            category='Fruit'
        )

        inventory_1 = Inventory.objects.create(
            user=new_user,
        )
        inventory_1.items.set([new_item_1.item_id, new_item_2.item_id])
        inventory_1.save()

        inventory_2 = Inventory.objects.create(
            user=superuser,
        )
        inventory_2.items.set([new_item_2.item_id, new_item_3.item_id])
        inventory_2.save()

        self.valid_token_normal, self.created = Token.objects.get_or_create(user=new_user)
        self.valid_token_admin, self.created = Token.objects.get_or_create(user=superuser)

        self.invalid_token = 'fasdfs45dsfasd1fsfasdf4dfassf13'

    def test_get_all_inventories_superuser(self):
        response = client.get(
            reverse('inventory:get_all_inventories'),
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token_admin.key),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_inventories_normal_authorized_user(self):
        response = client.get(
            reverse('inventory:get_all_inventories'),
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token_normal.key),
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_inventories_normal_unauthorized_user(self):
        response = client.get(
            reverse('inventory:get_all_inventories'),
            HTTP_AUTHORIZATION='Token {}'.format(self.invalid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_all_inventories_superuser_data_count(self):
        response = client.get(
            reverse('inventory:get_all_inventories'),
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token_admin.key),
        )
        self.assertEqual(len(response.data), 2)

    def test_get_all_inventories_superuser_data(self):
        response = client.get(
            reverse('inventory:get_all_inventories'),
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token_admin.key),
        )

        # Need to be done.
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CheckGetMyInventories(TestCase):
    """ Test module for get the inventories a specific user owns """

    def setUp(self):
        new_user = Account.objects.create(
            first_name='Danial',
            last_name='Bazmandeh',
            email='danibazi9@gmail.com',
            phone_number='+989152147655',
            gender='Male',
            password='123456'
        )

        new_item_1 = InventoryItem.objects.create(
            name='Test Item 1',
            quantity=5,
            unit='lb',
            location='Kitchen',
            category='Fruit'
        )

        new_item_2 = InventoryItem.objects.create(
            name='Test Item 2',
            quantity=10,
            unit='kg',
            location='Pantry',
            category='Fruit'
        )

        new_item_3 = InventoryItem.objects.create(
            name='Test Item 3',
            quantity=100,
            unit='kg',
            location='Cabinet',
            category='Fruit'
        )

        inventory_1 = Inventory.objects.create(
            user=new_user,
        )
        inventory_1.items.set([new_item_1.item_id, new_item_2.item_id])
        inventory_1.save()

        inventory_2 = Inventory.objects.create(
            user=new_user,
        )
        inventory_2.items.set([new_item_2.item_id, new_item_3.item_id])
        inventory_2.save()

        self.valid_token, self.created = Token.objects.get_or_create(user=new_user)
        self.invalid_token = 'fasdfs45dsfasd1fsfasdf4dfassf13'

    def test_get_my_inventories_authorized(self):
        response = client.get(
            reverse('inventory:get_my_inventories'),
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token.key),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_my_inventories_unauthorized(self):
        response = client.get(
            reverse('inventory:get_my_inventories'),
            HTTP_AUTHORIZATION='Token {}'.format(self.invalid_token),
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_my_inventories_data_count(self):
        response = client.get(
            reverse('inventory:get_my_inventories'),
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token.key),
        )
        self.assertEqual(len(response.data), 2)

    def test_get_all_inventories_data(self):
        response = client.get(
            reverse('inventory:get_my_inventories'),
            HTTP_AUTHORIZATION='Token {}'.format(self.valid_token.key),
        )

        # Need to be done.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
