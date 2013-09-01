# Create your views here.
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Permission

from shopping_cart.models import Store, Item

#### Stores ##########
@login_required
def home(request):
	stores = Store.objects.all()
	return render(request, 'shopping_cart/select_store.html', {'stores': stores})

@login_required
def store_homepage(request, store_id, ordered=False):
	print "storehome"
	print request.session['cart']
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
	print request
	if request.method == "POST":
		item_id = request.POST.get('item_id')
		name = request.POST.get('item_name')
		price = request.POST.get('item_price')
		quantity = request.POST.get('quantity')
		try:
			request.session['cart'].append({
				'item_id': item_id, 
				'quantity': quantity, 
				'name': name, 
				'price': price
				})
			# needed to save the session since we are
			# not modifying the session, but rather the
			# cart so it does not save.
			request.session.modified = True
		except:
			print "cart exception"
			request.session['cart'] = []
			request.session['cart'].append({
				'item_id': item_id, 
				'quantity': quantity, 
				'name': name, 
				'price': price
				})
			request.session.modified = True
		print request.session['cart']
		i = Item.objects.get(pk=item_id)
		return store_homepage(request, i.store.id, ordered=True)

def view_cart(request):
	print request.session['cart']
	return render(request, "shopping_cart/cart.html", {'cart_items':request.session['cart']})

def previous_orders(request):
	p_orders = Orders.objects.all().filter(buyer=request.user).order_by(reverse=True)
	return render(request, "shopping_cart/previous_orders.html", {'p_orders':p_orders})
