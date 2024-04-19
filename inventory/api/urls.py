from django.urls import path
from inventory.api import views

app_name = 'inventory'

urlpatterns = [
    path('all/', views.get_all_inventories, name='get_all_inventories'),
    path('me/', views.MyInventory.as_view(), name='my_inventory'),
    path('items/', views.InventoryItemCRUD.as_view(), name='inventory_items'),
    path('locations/', views.LocationCRUD.as_view(), name='locations'),
    # New URL patterns for Shopping List
    path('shopping-lists/', views.shopping_list, name='shopping-lists'),
    path('shopping-lists/<int:pk>/', views.shopping_list_detail, name='shopping-list-detail'),
    path('shopping-lists/<int:list_pk>/items/', views.add_item_to_shopping_list, name='add-item-to-shopping-list'),
    path('shopping-lists/<int:list_pk>/items/<int:item_pk>/', views.modify_or_remove_item_from_list, name='modify-or-remove-item-from-list'),
]
