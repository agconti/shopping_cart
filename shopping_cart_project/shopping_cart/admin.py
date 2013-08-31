#admin.py
from django.contrib import admin
from shopping_cart.models import Store, Item, Order

class ItemInline(admin.TabularInline):
	model = Item
	extra = 3

class StoreAdmin(admin.ModelAdmin):
	list_display = ('name','bio')
	fieldsets = [
				( 'Store Information', {'fields': ['name','bio',], 'classes': ['collapse']}),
	]
	
	exclude = ('owner',)
	inlines = [ItemInline]
    
class ItemAdmin(admin.ModelAdmin):
	list_display = ('name','price', 'quantity', 'description', 'store')
	search_fields = ['name','store__name', 'price', 'quantity']
	list_filter = ['store__name', 'date_added']

admin.site.register(Store, StoreAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Order)