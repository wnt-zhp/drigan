from django.conf import settings
from django.conf.urls import include, patterns, url
from django.conf.urls.static import static
from django.contrib import admin
from drigan.views import StartView
# Uncomment the next two lines to enable the admin:

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', StartView.as_view()),
    url(r'^events/', include('events.urls')),
    url(r'^forms/', include('DynamicForms.urls')),

    # Examples:
    # url(r'^$', 'drigan.views.home', name='home'),
    # url(r'^drigan/', include('drigan.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),


    url(r'^accounts/', include('drigan_registration.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
