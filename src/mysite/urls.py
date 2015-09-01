from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.conf.urls.i18n import i18n_patterns
import notifications

from usr.views import RegisterWizard, FORMS

from django.views.i18n import set_language

import settings

from django.contrib import admin
admin.autodiscover()


urlpatterns = [
    url(r'^ajax/', include('ajax.urls', namespace='ajax')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^select2/', include('django_select2.urls'))
]

urlpatterns += i18n_patterns('',
    # url('^inbox/notifications/', include(notifications.urls)),
    url(r'^$', 'usr.views.index', name='index'),
    url(r'^register/$', RegisterWizard.as_view(FORMS), name='register'),
    url(r'^usr/', include('usr.urls', namespace='usr')),
    #app for ajax requests
    url(r'^books/', include('books.urls',namespace='books')),
    url(r'^messages/', include('user_messages.urls', namespace='user_messages')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^test/', 'usr.views.test'),
    url(r'^', include('manager.urls', namespace='manager')),
)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
