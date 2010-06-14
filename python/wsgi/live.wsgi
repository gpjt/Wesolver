import os, sys
from os.path import dirname, join, normpath

MY_DIR = dirname(__file__)
PYTHON_ROOT = normpath(join(MY_DIR, ".."))
sys.path.append(PYTHON_ROOT)
os.environ['DJANGO_SETTINGS_MODULE'] = 'wesolver.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
