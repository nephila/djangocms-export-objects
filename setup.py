#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')
requirements = open('requirements.txt').readlines()
test_requirements = open('djangocms_export_objects/tests/requirements.txt').readlines()

# Add Python 2.6-specific dependencies
if sys.version_info[:2] < (2, 7):
    requirements.append('argparse')
    requirements.append('ordereddict')
    test_requirements.append('unittest2')

setup(
    name='djangocms_export_objects',
    version='0.1.0',
    description='A django CMS command to export PlaceholderFields-enable objects and all their dependencies',
    long_description=readme + '\n\n' + history,
    author='Iacopo Spalletti',
    author_email='i.spalletti@nephila.it',
    url='https://github.com/nephila/djangocms-export-objects',
    packages=find_packages(),
    #package_dir={'djangocms_export_objects': 'djangocms_export_objects'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='djangocms_export_objects',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='runtests.main',
    tests_require=test_requirements,
)
