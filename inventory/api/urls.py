from django.urls import path
from inventory.api import views

app_name = 'inventory'

urlpatterns = [
    path('all/', views.get_all_inventories, name='get_all_inventories'),
    path('me/', views.MyInventory.as_view(), name='my_inventory'),
    path('items/', views.InventoryItemCRUD.as_view(), name='inventory_items'),
    path('locations/', views.LocationCRUD.as_view(), name='locations'),
    # New URL patterns for Shopping List
    path('shopping-lists/', views.shopping_list_view, name='shopping_lists'),
    path('shopping-lists/<int:list_id>/', views.shopping_list_detail_view, name='shopping_list_detail'),
]
