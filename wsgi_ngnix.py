import os,sys

if not os.path.dirname(__file__) in sys.path[:1]:
	sys.path.insert(0, os.path.dirname(__file__))
os.environ['DJANGO_SETTINGS_MODULE'] = 'DjangoDemo.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
