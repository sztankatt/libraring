from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$', 'realtime_test.views.home', name='home'),
	url(r'^alert/$', 'realtime_test.views.alert', name='alert'),
)