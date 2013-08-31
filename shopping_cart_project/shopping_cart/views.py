# Create your views here.
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Permission

from shopping_cart.models import Store, Item

@login_required
def home(request):
	return render(request, 'shopping_cart/base.html')


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