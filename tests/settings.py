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
    'django.contrib.admin',
    "django.contrib.auth",
    "django.contrib.contenttypes",
    'django.contrib.messages',
    "django.contrib.sites",
    "geonames_place",
]

SITE_ID = 1

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ]
        }
    }
]

ROOT_URLCONF = 'geonames_place.urls'

GEONAMES_KEY = os.environ.get('GEONAMES_KEY')
GEONAMES_MAX_RESULTS = 10
