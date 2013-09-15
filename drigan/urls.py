from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin

from drigan.views import StartView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', StartView.as_view()),
    url(r'^events/', include('events.urls')),

    # Examples:
    # url(r'^$', 'drigan.views.home', name='home'),
    # url(r'^drigan/', include('drigan.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),


    url(r'^accounts/', include('drigan_registration.urls')),
)
