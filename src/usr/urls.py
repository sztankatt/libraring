from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    '',
    url(r'^$', 'usr.views.load_profile', name='own_profile'),
    url(r'^login/$', 'usr.views.login_view', name='login'),
    url(r'^logout/$', 'usr.views.logout_view', name='logout'),
   
    # blocked profile handling views
    url(
        r'^blocked-profile/$',
        'usr.views.blocked_profile',
        name='blocked_profile'),
    url(
        r'^register/confirmation/(?P<confirmation_code>[a-zA-Z0-9]{50})/$',
        'usr.views.register_confirmation_code',
        name='register_confirmation_code'),

    url(
        r'^register/confirmation/$',
        'usr.views.register_confirmation',
        name='register_confirmation'),
    url(
        r'^new/email/confirmation/$',
        'usr.views.new_email_confirmation',
        name='new_email_confirmation'),
    url(
        r'^deactivated/profile/$',
        'usr.views.deactivated_profile',
        name='deactivated_profile'),
    url(
        r'add/previous/education/$',
        'usr.views.add_previous_education',
        name='add_previous_education'),
    url(
        r'^notifications/$',
        'usr.views.notifications',
        name='notifications'),
    url(
        r'add/notifications/read/(?P<id>[0-9]+)/$',
        'usr.views.notifications_read',
        name='notifications_read')
)
