"""
WSGI config for obviously project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "obviously.settings")

application = get_wsgi_application()

# As we are using an in-memory db, we need to run migrations each time we start the server / tests
call_command("makemigrations")
call_command("migrate")
