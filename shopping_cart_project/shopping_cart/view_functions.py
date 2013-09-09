### Aux functions for the views ############
### moved here to keep the views skinny ####

def add_item(request):
	item_id = request.POST.get('item_id')
	name = request.POST.get('item_name')
	price = request.POST.get('item_price')
	quantity = request.POST.get('quantity')
	shipping = request.POST.get('shipping_choices')
	try:
		# add an item to the cart if there is a cart
		request.session['cart'].append({
			'item_id': item_id, 
			'quantity': quantity, 
			'name': name, 
			'price': price,
			'shipping':shipping
			})
		# This is needed to save the session since 
		# we are not modifying the session, but 
		# rather the item in the session dict. 
		request.session.modified = True
	except:
		# create an empty cart
		request.session['cart'] = []
		request.session['cart'].append({
			'item_id': item_id, 
			'quantity': quantity, 
			'name': name, 
			'price': price,
			'shipping':shipping
			})
		request.session.modified = True
	return item_id
	
def chart_prep(cart):
	import pandas as pd
	import numpy as np
	import json
	shipping = {'ground': 4.35, 'snail': 14.43, 'owl': 5.00, 'teleporter':324.04, 'pony_express':45.28}
	tax = .10


	df = pd.DataFrame(cart, dtype=np.float16)
	# munge data to compute totals and order percentage breakdown 
	df['shipping_costs'] = df.shipping.apply(lambda x: shipping[x])
	df['tax'] = (((df.price * df.quantity)+ df.shipping_costs ) * tax)
	df['total_price'] = ((df.price * df.quantity) + df.tax + df.shipping_costs)
	total = df.total_price.sum()
	# create an array with break down of item, shipping, and tax costs as a percentage of the order
	a = [
			((df.price * df.quantity).sum()/ total), 
			df.shipping_costs.sum() / total,
			df.tax.sum() / total
		]
	# prepare array for d3 
	return json.dumps(a)