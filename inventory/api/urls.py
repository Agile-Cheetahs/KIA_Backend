from django.urls import path
from inventory.api import views

app_name = 'inventory'

urlpatterns = [
    path('all/', views.get_all_inventories, name='get_all_inventories'),
    path('me/', views.get_my_inventories, name='get_my_inventories'),
    path('items/', views.InventoryItemCRUD.as_view(), name='inventory_items'),
]