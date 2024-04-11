from django.urls import path
from inventory.api import views

app_name = 'inventory'

urlpatterns = [
    path('all/', views.get_all_inventories, name='get_all_inventories'),
    path('me/', views.MyInventory.as_view(), name='my_inventory'),
    path('items/', views.InventoryItemCRUD.as_view(), name='inventory_items'),
]