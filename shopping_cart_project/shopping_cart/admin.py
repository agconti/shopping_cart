#admin.py
from django.contrib import admin
from shopping_cart.models import Store, Item, Order
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _

# class StoreUser_ListFilter(SimpleListFilter):
# 	title = _("Store")
# 	parameter_name = 'owner'
# 	def queryset(self, request, queryset):
# 		return Store.objects.all().filter(owner=request.user)

class ItemInline(admin.TabularInline):
	model = Item
	extra = 3

class StoreAdmin(admin.ModelAdmin):
	list_display = ('name','bio')
	# fieldsets = [
	# 			( 'Store Information', {'fields': ['name', 'owner', 'bio',]})
	# ],
	inlines = (ItemInline, )
    
class ItemAdmin(admin.ModelAdmin):
	list_display = ('name','price', 'quantity', 'description', 'store')
	search_fields = ['name', 'price', 'quantity', 'store__name']
	list_filter = ('store__name','store__owner', 'date_added')

	#filter returned item list by owner, so merchants only see thier items
	def queryset(self, request):
		qs = super(ItemAdmin, self).queryset(request)
		return qs.filter(store__owner=request.user)

admin.site.register(Store, StoreAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Order)