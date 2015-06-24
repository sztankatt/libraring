from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'user_messages.views.main', name='main'),
    url(r'^(?P<transaction_id>\d+)/$',
        'user_messages.views.conversation', name='conversation'),
    url(r'^add/new/message/$', 'user_messages.views.add_new_message', name='add_new_message'),
    url(r'^transaction/accept/$', 'books.views.transaction_accept', name='transaction_accept'),
    url(r'^transaction/(?P<pk>[0-9]+)/rate/$', 'books.views.transaction_rate', name='transaction_rate'),
)