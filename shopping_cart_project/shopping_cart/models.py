from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
import datetime

# Create your models here.
class Store(models.Model):
	name = models.CharField(max_length=200)
	bio = models.TextField()
	owner = models.OneToOneField(User)

	def __unicode__(self):
		'''
		for human readable model representation 
		'''
		return "Store %s: by Merchant %s" %(self.name, self.owner.username)

class Item(models.Model):
	store = models.ForeignKey('Store')
	name = models.CharField(max_length=200)
	description = models.TextField()
	price = models.DecimalField(max_digits=19, decimal_places=2)
	quantity = models.IntegerField(validators=[MinValueValidator(0)])
	date_added = models.DateTimeField(auto_now_add=True)
	
	@property
	def recomend(self, transaction):
		'''
		simple recommendation engine. 
		'''
		items = Item.objects.values('id','price')
		# find the product with the closest proximity to user spending habits
		recomend_item = min(items, key=lambda k: (items[k] - transaction.avg_transaction))
		return Item.objects.get(pk=recomend_item.items()[0][0])


	
	def in_stock(self):
		'''
		Checks if an item is in stock.
		'''
		if self.quantity > 0:
			return True
		else:
			return	False

		def __unicode__(self):
		'''
		for human readable model representation 
		'''
		return "Item: %s: Sold by %s" %(self.name, self.store.name)

class Order(models.Model):
	shipping_choices = [
					('ground', 'Ground'),
					('snail', 'Snail'),
					('owl', 'Owl'),
					('teleporter', 'Teleporter'),
					('pony_express', 'Pony Express'),
				]		
	shipping = models.CharField(max_length=200,
								choices=shipping_choices,
                                default='ground')
	buyer = models.ForeignKey(User)
	date_ordered = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		'''
		for human readable model representation 
		'''
		return "Order by %s: on %s" %(self.buyer.username, self.date_ordered.ctime())

class Transaction(models.Model):
	order = models.ForeignKey(Order)
	item = models.ForeignKey(Item)
	# Min value is set to 1 to make sure some one actually orders an item 
	quantity = models.IntegerField(validators=[MinValueValidator(1)])

	@property 
	def avg_transaction(self):
		'''
		go through a users orders and get their avg_transaction (item) price
		'''
		avg_transaction = 0 
		user = self.order.buyer
		orders = Order.objects.filter(buyer=user)
		for i,o in enumerate(orders):
			avg_purchase = 0
			for t in o.transaction_set:
				sum_purchase += t.item.price
			avg_purchase = (sum__purchase / float(len(o.transaction_set)))
			avg_transaction = ((avg_transaction + avg_purchase) / float(i))
		return avg_transaction





	def __unicode__(self):
		'''
		for human readable model representation 
		'''
		return "Order %s: on %s" %(self.order, self.order.date_ordered.ctime())


