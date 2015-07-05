from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from usr.views import RegisterWizard, FORMS

import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'usr.views.index', name='index'),
    url(r'^register/$', RegisterWizard.as_view(FORMS), name='register'),
    #url(r'^polls/', include('polls.urls', namespace='polls')),
    url(r'^usr/', include('usr.urls', namespace='usr')),
    #app for ajax requests
    url(r'^ajax/', include('ajax.urls', namespace='ajax')),
    url(r'^books/', include('books.urls',namespace='books')),
    url(r'^messages/', include('user_messages.urls', namespace='user_messages')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^test/', 'usr.views.test'),
    url(r'^select2/', include('django_select2.urls')),
    url(r'^', include('manager.urls', namespace='manager')),
)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
