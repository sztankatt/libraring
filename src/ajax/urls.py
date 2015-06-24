from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
        url(r'^email/ending/$', 'ajax.views.get_email_ending'),
        url(r'^update/profile/$', 'ajax.views.update_profile'),
        url(r'^get/error/message/$', 'ajax.views.get_error_message'),
        url(r'^email/change/confirmation/$', 'ajax.views.email_change_confirmation'),
        url(r'^add/to/watchlist/$', 'ajax.views.add_to_watchlist'),
        url(r'^upload/new/book/$', 'ajax.views.upload_new_book'),
        url(r'^list/books/$', 'ajax.views.list_books'),
        url(r'^check/username/available/$', 'ajax.views.check_username_available'),
        url(r'^load/conversation/$', 'ajax.views.load_conversation'),
        url(r'^check/email/ending/$', 'ajax.views.check_email_ending'),
        url(r'^load/all/books/$', 'ajax.views.load_all_books'),
        url(r'^rate/transaction/$', 'ajax.views.rate_transaction')
    )