from django.contrib import admin

from inventory.models import *


# Register your models here.
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ['item_id', 'name', 'quantity', 'units', 'location', 'expiration_date', 'category']
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
