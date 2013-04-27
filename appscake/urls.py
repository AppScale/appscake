""" Maps URL AppsCake UI paths to rendering functions in views.py. """
from django.conf.urls import patterns
from django.conf.urls import url

URL_PATTERNS = patterns('appscake.views',
    url(r'^$', 'home', name='home'),
    (r'^about/$', 'about',),
    (r'^common/.*', 'common',),
    url(r'start/$', 'start'),
    url(r'terminate/$', 'terminate'),
    url(r'test/$', 'test'),
    url(r'getdeploymentstatus/$', 'get_deployment_status'),
    url(r'getterminationstatus/$', 'get_termination_status')
    )



