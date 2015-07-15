from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
        url(r'^email/ending/$', 'ajax.views.get_email_ending', name='get_email_encoding'),
        url(r'^update/profile/$', 'ajax.views.update_profile', name='udate_profile'),
        url(r'^get/error/message/$', 'ajax.views.get_error_message', name='get_error_message'),
        url(r'^email/change/confirmation/$', 'ajax.views.email_change_confirmation', name='email_change_confirmation'),
        url(r'^add/to/watchlist/$', 'ajax.views.add_to_watchlist', name='add_to_watchlist'),
        url(r'^upload/new/book/$', 'ajax.views.upload_new_book', name='upload_new_book'),
        url(r'^list/books/$', 'ajax.views.list_books', name='list_books'),
        url(r'^check/username/available/$', 'ajax.views.check_username_available', name='check_username_available'),
        url(r'^load/conversation/$', 'ajax.views.load_conversation', name='load_conversation'),
        url(r'^check/email/ending/$', 'ajax.views.check_email_ending', name='check_email_ending'),
        url(r'^load/all/books/$', 'ajax.views.load_all_books', name='load_all_books'),
        url(r'^rate/transaction/$', 'ajax.views.rate_transaction', name='rate_transaction')
    )