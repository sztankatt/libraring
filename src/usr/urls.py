from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$', 'usr.views.load_profile', name='own_profile'),
	url(r'^(?P<id>\d+)/$', 'usr.views.load_profile', name='profile'),
        #url(r'^(?P<pk>\d+)/books/$', books_views.books, name='own_books'),
        url(r'^login/$', 'usr.views.login_view', name='login'),
        url(r'^logout/$', 'usr.views.logout_view', name='logout'),
        
        #blocked profile handling views
        url(r'^blocked-profile/$', 'usr.views.blocked_profile', name='blocked_profile'),
        url(r'^register/confirmation/(?P<confirmation_code>[a-zA-Z0-9]{50})/$', 'usr.views.register_confirmation_code',\
            name='register_confirmation_code'),
        
        url(r'^register/confirmation/$', 'usr.views.register_confirmation', name='register_confirmation'),
        url(r'^new/email/confirmation/$', 'usr.views.new_email_confirmation', name='new_email_confirmation'),
        url(r'^deactivated/profile/$', 'usr.views.deactivated_profile', name='deactivated_profile'),
        
        #changing profile views
        #url(r'change/current/education/$', 'usr.views.change_current_education', name='change_current_education'),
        url(r'add/previous/education/$', 'usr.views.add_previous_education', name='add_previous_education')
)
