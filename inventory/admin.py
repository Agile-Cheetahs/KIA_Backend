from django.contrib import admin

from inventory.models import *


# Register your models here.
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ['item_id', 'name', 'quantity', 'unit', 'location', 'expiration_date', 'category']
    search_fields = ['name', 'location', 'category']
    list_filter = ['location', 'category']

    class Meta:
        model = InventoryItem


admin.site.register(InventoryItem, InventoryItemAdmin)


class InventoryAdmin(admin.ModelAdmin):
    list_display = ['inventory_id', 'user', 'get_items',]
    search_fields = ['user__first_name', 'user__last_name']
    list_filter = ['user']

    def get_items(self, obj):
        results = obj.items.all()
        return ', '.join([item.__str__() for item in results])
    get_items.short_description = 'Items'

    class Meta:
        model = Inventory


admin.site.register(Inventory, InventoryAdmin)

# New admin for ShoppingListItem
# Admin Class for ShoppingListItem
class ShoppingListItemAdmin(admin.ModelAdmin):
    list_display = ['item_id', 'name', 'quantity', 'units', 'crossed']
    search_fields = ['name']
    list_filter = ['crossed']

admin.site.register(ShoppingListItem, ShoppingListItemAdmin)

# Admin Class for ShoppingList
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ['list_id', 'name', 'display_items', 'is_favorite', 'is_complete']
    search_fields = ['name']
    list_filter = ['is_favorite', 'is_complete']

    def display_items(self, obj):
        return ', '.join([item.name for item in obj.items.all()])
    display_items.short_description = 'Items in List'

admin.site.register(ShoppingList, ShoppingListAdmin)