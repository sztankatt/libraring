from django.conf.urls import patterns, include, url
from haystack.forms import ModelSearchForm, SearchForm
from haystack.query import SearchQuerySet
from haystack.views import SearchView

urlpatterns = patterns('',
	#url(r'^$', 'books.views.main_page', name='main_page'),
        #url(r'^search/', include('haystack.urls')),
    url(r'^usr/(?P<rtype>[A-Za-z]+)/$', 'books.views.usr_book_page', name='main_page'),
    url(r'^search/', SearchView(
        template='after_login/books/search_page.html',
        form_class=SearchForm
    ), name='haystack_search'),
    url(r'^book/(?P<id>[0-9]+)/$', 'books.views.book_page', name='book_page'),
    url(r'^genre/(?P<name>[A-Za-z]+)/$', 'books.views.genre', name='genre'),
    url(r'^author/(?P<pk>[0-9]+)/$', 'books.views.author', name='author'),
    url(r'^publisher/(?P<pk>[0-9]+)/$', 'books.views.publisher', name='publisher'),
    url(r'^make/an/offer/$', 'books.views.make_an_offer', name='offer'),
    url(r'^delete/the/offer/$', 'books.views.delete_the_offer', name='delete_the_offer'),
    url(r'^accept/the/offer/$', 'books.views.accept_the_offer', name='accept_the_offer'),
    url(r'^finalise/transaction/$', 'books.views.finalise_transaction', name='finalise_transaction'),
    url(r'^rate/transaction/$', 'books.views.rate_transaction', name='rate_transaction'),
    url(r'^upload/new/book/$', 'books.views.upload_new_book', name='upload_new_book'),
    url(r'^detailed/upload/new/book/$',
        'books.views.detailed_upload_new_book', name='detailed_upload_new_book')
)
