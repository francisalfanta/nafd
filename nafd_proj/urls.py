import autocomplete_light
# import every app/autocomplete_light_registry.py
autocomplete_light.autodiscover()

from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from ccad.admin_helpers import *


admin.autodiscover()

urlpatterns = patterns('',
	url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^admin/', include(admin_site.urls)),
    url(r'^logs/', include('ccad.urls'), name='logs'),       
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),    
   
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()