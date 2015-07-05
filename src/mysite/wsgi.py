import sys
sys.path += ['/home/libraring/lib/python2.7',]
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
