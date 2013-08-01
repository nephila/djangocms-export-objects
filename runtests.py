#!/usr/bin/env python
from __future__ import with_statement
import django
from djangocms_export_objects.tests.cli import configure
from djangocms_export_objects.tests.tmpdir import temp_dir
import argparse
import sys

import os

os.environ['DJANGO_SETTINGS_MODULE'] = "djangocms_export_objects.tests.settings"

def main(time_tests=False, verbosity=1, failfast=False, test_labels=None):
    sys.path.insert(0, os.path.dirname(__file__))
    with temp_dir() as STATIC_ROOT:
        with temp_dir() as MEDIA_ROOT:
            configure(STATIC_ROOT=STATIC_ROOT, MEDIA_ROOT=MEDIA_ROOT,
                      TEST_RUNNER='discover_runner.DiscoverRunner')
            from django.conf import settings
            from django.test.utils import get_runner
            TestRunner = get_runner(settings)

            test_runner = TestRunner(verbosity=verbosity, interactive=False,
                                     failfast=failfast)
            if not test_labels:
                test_labels = ['djangocms_export_objects.tests']
            failures = test_runner.run_tests(test_labels)
    sys.exit(failures)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--failfast', action='store_true', default=False,
                        dest='failfast')
    parser.add_argument('--verbosity', default=1)
    parser.add_argument('--time-tests', action='store_true', default=False,
                        dest='time_tests')
    parser.add_argument('test_labels', nargs='*')
    args = parser.parse_args()

    time_tests = getattr(args, 'time_tests', False)
    test_labels = None
    if args.test_labels:
        test_labels = ['djangocms_export_objects.tests.%s' % label for label in args.test_labels]
    main(time_tests=time_tests, verbosity=int(args.verbosity),
         failfast=args.failfast, test_labels=test_labels)
