from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns(
    '',
    url(r'^our-team/$', TemplateView.as_view(
        template_name='before_login/manager/our_team.html'),
        name='our_team'),

    url(r'^tour/$', TemplateView.as_view(
        template_name='before_login/manager/tour.html'),
        name='tour'),

    url(r'^brainstorm/$',
        'manager.views.brainstorm',
        name='brainstorm'),

    url(r'^terms-and-conditions/$', TemplateView.as_view(
        template_name='before_login/manager/terms_conditions.html'),
        name='terms_conditions'),

    url(r'^privacy-policy/$', TemplateView.as_view(
        template_name='before_login/manager/privacy.html'),
        name='privacy'),
)
