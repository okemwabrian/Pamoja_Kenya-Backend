import os
import sys

# Add your project directory to Python path
path = '/home/Okemwabrianny/pamoja_backend'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamoja_kenya.settings_production')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()