# Create your views here.
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Permission

from shopping_cart.models import Store, Item, Order, Transaction

#### Stores ##########
@login_required
def home(request):
	stores = Store.objects.all()
	return render(request, 'shopping_cart/select_store.html', {'stores': stores})

@login_required
def store_homepage(request, store_id, ordered=False):
	#get the store's name from the subdomain or the passed store id. 
	try:
		s = get_object_or_404(Store, name=request.subdomain) 
		Items = Item.objects.all().filter(store=s)
		
	except:
		s = get_object_or_404(Store, pk=store_id) 
		Items = Item.objects.all().filter(store=s)

	return render(request, "shopping_cart/store_homepage.html", {'Items':Items, 'ordered':ordered})


##### Handel login / logout #######
def logout_view(request):
    logout(request)

def create_user(request):
	'''
	create and login user
	'''
	if request.method == 'POST':
		form = UserCreationForm(request.POST)	
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password2')
			form.save()
			#login user
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
			    	return HttpResponseRedirect('/')
	else:
		form = UserCreationForm()
	return render(request, 'shopping_cart/create_user.html', {'form': form})

### shopping_cart ###
@login_required
def add_to_cart(request):
	if request.method == "POST":
		item_id = request.POST.get('item_id')
		name = request.POST.get('item_name')
		price = request.POST.get('item_price')
		quantity = request.POST.get('quantity')
		try:
			# add an item to the cart if there is a cart
			request.session['cart'].append({
				'item_id': item_id, 
				'quantity': quantity, 
				'name': name, 
				'price': price
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
				'price': price
				})
			request.session.modified = True
		i = Item.objects.get(pk=item_id)
		return store_homepage(request, i.store.id, ordered=True)

def view_cart(request): 
	if request.method == "GET":
		recommendations = Item.recommend
		print recommendations
		if request.session.get('cart', default=None) != None:
			return render(request, "shopping_cart/cart.html", {
				'cart_items': request.session['cart'], 
				'recommendations':recommendations
				})
		else:
			return render(request, "shopping_cart/empty_cart.html", {'recommendations':recommendations})

def checkout(request):
	if request.method == "GET":
		# Create order first
		o = Order.objects.create(buyer=request.user)
		# add items to order
		for i in request.session['cart']:
			Transaction.objects.create(
				order = o, 
				item=Item.objects.get(pk=i['item_id']), 
				quantity=i['quantity']
				)
		# empty cart
		del request.session['cart']
		return render(request, "shopping_cart/order_processed.html", {'order': o})



def previous_orders(request):
	p_orders = Order.objects.all().filter(buyer=request.user).reverse()
	return render(request, "shopping_cart/previous_orders.html", {'p_orders':p_orders})
