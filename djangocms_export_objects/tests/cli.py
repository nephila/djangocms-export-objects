# -*- coding: utf-8 -*-
import os
import logging

gettext = lambda s: s

urlpatterns = []


def configure(**extra):
    from django.conf import settings
    defaults = dict(
        CACHE_BACKEND='locmem:///',
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        SOUTH_TESTS_MIGRATE=False,
        PASSWORD_HASHERS=(
            'django.contrib.auth.hashers.MD5PasswordHasher',
        )
    )
    defaults.update(extra)
    for key, value in defaults.items():
        setattr(settings, key, value)
    from south.management.commands import patch_for_test_db_setup
    patch_for_test_db_setup()
    logging.disable(logging.CRITICAL)
