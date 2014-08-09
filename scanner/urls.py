from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

guid_re = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

urlpatterns = patterns('',
    url(r'^scan/(?P<api_key_guid>%s)/(?P<scanner_name>[^/])/(?P<target>.+)$' % guid_re, 'scan.views.scan'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'.*', 'scan.views.bounce'),
)
