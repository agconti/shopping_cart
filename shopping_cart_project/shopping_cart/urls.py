from django.conf.urls import patterns, url
from shopping_cart import views
from shopping_cart_project import settings

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^create_user/', views.create_user, name='create_user'),
)