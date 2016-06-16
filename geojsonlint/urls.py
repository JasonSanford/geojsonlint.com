from django.conf.urls import patterns, include, url
from django.conf import settings

from .views import home, validate

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', home, name='home'),
    url(r'^validate$', validate, name='validate'),
    # url(r'^geojsonlint/', include(foo.urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include(django.contrib.admindocs.urls)),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
]
