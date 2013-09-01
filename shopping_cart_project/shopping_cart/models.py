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
	price = models.DecimalField(max_digits=19, decimal_places=2)
	description = models.TextField()
	quantity = models.IntegerField(validators=[MinValueValidator(0)])
	date_added = models.DateTimeField(auto_now_add=True)
	def __unicode__(self):
		'''
		for human readable model representation 
		'''
		return "Item: %s: Sold by %s" %(self.name, self.store.name)
	def in_stock(self):
		'''
		Check if item is in stock
		'''
		if self.quantity > 0:
			return True
		else:
			return	False

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
	item = models.ForeignKey(Item)
	quantity = models.IntegerField(validators=[MinValueValidator(0)])
	buyer = models.OneToOneField(User)
	date_ordered = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		'''
		for human readable model representation 
		'''
		return "Order by %s: on %s" %(self.buyer.username, self.date_ordered.ctime())


