from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
import datetime

# Create your models here.
class Merchant(models.Model):
	name = models.CharField(max_length=200, unique=True)
	user = models.OneToOneField(User)

	def __unicode__(self):
		'''
		for human readable model representation 
		'''
		return "Merchant %s : Manager %s" %(self.name, self.user.username)

class Store(models.Model):
	name = models.CharField(max_length=200)
	bio = models.TextField()
	owner = models.OneToOneField(Merchant)

	def __unicode__(self):
		'''
		for human readable model representation 
		'''
		return "Store %s: by Merchant %s" %(self.name, self.owner.name)

class Item(models.Model):
	name = models.CharField(max_length=200)
	prices = models.DecimalField(max_digits=19, decimal_places=2)
	description = models.TextField()
	quantity = models.IntegerField(validators=[MinValueValidator(0)])
	date_added = models.DateTimeField(auto_now_add=True)
	store = models.OneToOneField(Store)

	def __unicode__(self):
		'''
		for human readable model representation 
		'''
		return "Item: %s: Sold by %s" %(self.name, self.store.name)

class Order(models.Model):
	item = models.OneToOneField(Item)
	quantity = quantity = models.IntegerField(validators=[MinValueValidator(0)])
	user = models.OneToOneField(User)
	date_ordered = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		'''
		for human readable model representation 
		'''
		return "Order by %s: on %s" %(self.user.username, self.date_ordered.ctime())


