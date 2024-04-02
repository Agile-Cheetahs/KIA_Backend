from django.test import TestCase

from account.models import Account
from inventory.models import InventoryItem, Inventory


class InventoryItemTest(TestCase):
    """ Test module for Inventory Item model """

    def setUp(self):
        InventoryItem.objects.create(
            name='Test Item',
            quantity=5,
            unit='lb',
            location='Kitchen',
            category='Fruit'
        )

    def test_inventory_item_str(self):
        item = InventoryItem.objects.get(name='Test Item')
        self.assertEqual(item.__str__(), 'Test Item - 5 lb')

    def test_inventory_item_quantity(self):
        item = InventoryItem.objects.get(name='Test Item')
        self.assertEqual(item.quantity, 5)

    def test_inventory_item_unit(self):
        item = InventoryItem.objects.get(name='Test Item')
        self.assertEqual(item.unit, 'lb')

    def test_inventory_item_location(self):
        item = InventoryItem.objects.get(name='Test Item')
        self.assertEqual(item.location, 'Kitchen')

    def test_inventory_item_category(self):
        item = InventoryItem.objects.get(name='Test Item')
        self.assertEqual(item.category, 'Fruit')


class InventoryTest(TestCase):
    """ Test module for Inventory model """

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

        inventory = Inventory.objects.create(
            user=new_user,
        )
        inventory.items.set([new_item_1.item_id, new_item_2.item_id])
        inventory.save()

    def test_inventory_str(self):
        user = Account.objects.get(email='danibazi9@gmail.com')
        inventory = Inventory.objects.get(user=user)
        self.assertEqual(inventory.__str__(), 'Inventory for Danial Bazmandeh')

    def test_inventory_user(self):
        user = Account.objects.get(email='danibazi9@gmail.com')
        inventory = Inventory.objects.get(user=user)
        self.assertEqual(inventory.user.user_id, user.user_id)

    def test_inventory_items(self):
        user = Account.objects.get(email='danibazi9@gmail.com')
        inventory = Inventory.objects.get(user=user)
        item_1 = InventoryItem.objects.get(name='Test Item 1')
        item_2 = InventoryItem.objects.get(name='Test Item 2')

        self.assertEqual(list(inventory.items.all()), [item_1, item_2])
