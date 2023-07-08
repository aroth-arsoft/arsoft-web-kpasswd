from django.conf.urls import include, url
from django.conf import settings
from arsoft.web.utils import django_debug_urls

from . import views
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', views.home, name='home'),
    url(r'^login$', views.login, name='login'),
    url(r'^changepw$', views.changepw, name='changepw'),
#    url(r'^%s$' % settings.BASE_URL, 'arsoft.web.kpasswd.views.home', name='home'),
#    url(r'^%s/changepw$' % settings.BASE_URL, 'arsoft.web.kpasswd.views.changepw', name='changepw'),
    # url(r'^arsoft.web.kpasswd/', include('arsoft.web.kpasswd.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^debug/', include(django_debug_urls())),
]
