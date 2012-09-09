import django
from django.conf import settings


if 'django.contrib.admin' in settings.INSTALLED_APPS:
    from vendors.guardian.tests.admin_test import *

if django.VERSION >= (1, 3):

