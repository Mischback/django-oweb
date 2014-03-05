from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'', include('oweb.urls', namespace='oweb')),
    url(r'', include('django.contrib.staticfiles.urls')),
)
