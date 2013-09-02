#### View Tests ####
import unittest
from django.test import TestCase
from django.test.client import Client
from shopping_cart.models import Store, Order, Item, Transaction
from django.contrib.auth.models import User

def login_test_user(self):
	self.client = Client()
	self.username = 'test_user'
	self.email = 'test@test.com'
	self.password = 'test'
	self.test_user = User.objects.create_user(self.username, self.email, self.password)
	login = self.client.login(username=self.username, password=self.password)
	self.assertEqual(login, True)

class Home_ViewTest(TestCase):
	def setUp(self):
		login_test_user(self)

	def test_details(self):
		# get the home view
		response = self.client.get('/')      
		self.assertEqual(response.status_code, 200)

		# Check that the rendered context is not none 
		self.assertTrue(response.context['stores'] != None)

	def tearDown(self):
		self.test_user.delete()

# class store_homepage_ViewTest(TestCase):
# 	def setUp(self):
# 		login_test_user(self)

# 	def test_details(self):

# 		#create store
# 		s = Store.objects.create(name="test_store", bio="Stuff", owner=self.test_user)
# 		Item.objects.create(store=s, name='Hook Hand', price=50, quantity=1)
# 		response = self.client.post('store_homepage/1/')
# 		print response.context
# 		# Check that the response is 200 OK.
# 		self.assertEqual(response.status_code, 200)

# 		# Check that the rendered context is not none 
# 		self.assertTrue(response.context['ordered'] != None)
# 		self.assertTrue(response.context['Items'] != None)  

	def tearDown(self):
		print "tear down"
		self.test_user.delete()

class logout_view_ViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_details(self):
    	# get the home view
        response = self.client.get('/accounts/logout/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.login(), False)

class create_user_ViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_details(self):
    	# get the home view
        response = self.client.get('/create_user/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

class add_to_cart_ViewTest(TestCase):
    def setUp(self):
        login_test_user(self)

    def test_details(self):
    	# get the home view
    	s = Store.objects.create(name="test_store", bio="Stuff", owner=self.test_user)
        Item.objects.create(store=s, name='Hook Hand', price=50, quantity=1)
        response = self.client.post('/add_to_cart/', {'item_id': u'1', 'name': u'Hook Hand', 'price': u'50', 'quantity': u'1'})

        # Check that the response is 302 Found.
        self.assertEqual(response.status_code, 200)

	def tearDown(self):
		self.test_user.delete()

        
class view_cart_ViewTest(TestCase):
    def setUp(self):
        login_test_user(self)

	def test_details(self):
		# get the home view
		response = self.client.get('/view_cart/')

		# Check that the response is 301 perm redirect.
		self.assertEqual(response.status_code, 200)

	def tearDown(self):
		self.test_user.delete()

class checkout_ViewTest(TestCase):
    def setUp(self):
        login_test_user(self)

	def test_details(self):
		# get the home view
		response = self.client.get('/checkout/')

		# Check that the response is 200 OK.
		self.assertEqual(response.status_code, 200)
		self.assertTrue(response.context['order'] != None)

	def tearDown(self):
		self.test_user.delete()


class previous_orders_ViewTest(TestCase):
    def setUp(self):
        login_test_user(self)

    def test_details(self):
    	# get the home view
        response = self.client.get('/previous_orders/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200) 

        self.assertTrue(response.context['p_orders'] != None)

	def tearDown(self):
		self.test_user.delete()