from django.conf.urls import patterns, url
from shopping_cart import views
from shopping_cart_project import settings

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^create_user/', views.create_user, name='create_user'),
    url(r'^store_homepage/(?P<store_id>\d+)/$', views.store_homepage, name='store_homepage'),
    url(r'^add_to_cart/', views.add_to_cart, name='add_to_cart'),
    url(r'^view_cart/', views.view_cart, name='view_cart'),
    url(r'^previous_orders/', views.previous_orders, name='previous_orders'),
    url(r'^checkout/', views.checkout, name='checkout'),

)
