# -*- coding: utf-8
from __future__ import absolute_import, unicode_literals

import os

import django

DEBUG = True
USE_TZ = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "#u2$)oc)wpm6c5k0eyiw5_p&9qhp+9l7p%wqg-2no0h9g2j1fe"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "geonames_place",
]

SITE_ID = 1

MIDDLEWARE_CLASSES = ()

GEONAMES_KEY = os.environ.get('GEONAMES_KEY')
GEONAMES_MAX_RESULTS = 10
