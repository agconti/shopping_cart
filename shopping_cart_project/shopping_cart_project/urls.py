from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^', include('shopping_cart.urls')),
    # url(r'^shopping_cart_project/', include('shopping_cart_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'shopping_cart/login.html'}, name='login_view'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',{'template_name': 'shopping_cart/base.html'}, name='logout_view'),
    url(r'^view_cart/', 'shopping_cart.views.view_cart', name='view_cart'),


)
