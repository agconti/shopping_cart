#### View Tests ####
import unittest
from django.test.client import Client

class HomeViewTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_details(self):
    	# get the home view
        response = self.client.get('/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that the rendered context is not none 
        self.assertTrue(response.context['stores'] != None)