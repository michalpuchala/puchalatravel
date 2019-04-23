"""
WSGI config for puchalatravel project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'puchalatravel.settings.prod')
project_folder = os.path.expanduser('/home/ubuntu/puchalatravel/')
load_dotenv(os.path.join(project_folder, '.env'))
application = get_wsgi_application()
