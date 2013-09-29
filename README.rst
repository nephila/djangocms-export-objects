===============================
django CMS Export Objects
===============================

#.. image:: https://badge.fury.io/py/djangocms-export-objects.png
#        :target: http://badge.fury.io/py/djangocms-export-object
    
.. image:: https://travis-ci.org/nephila/djangocms-export-objects.png?branch=master
        :target: https://travis-ci.org/nephila/djangocms-export-objects

#.. image:: https://pypip.in/d/djangocms-export-objects/badge.png
#        :target: https://crate.io/packages/djangocms-export-objects?version=latest

.. image:: https://coveralls.io/repos/nephila/djangocms-export-objects/badge.png
        :target: https://coveralls.io/r/nephila/djangocms-export-objects

A django CMS command to export cMS Pages and PlaceholderFields-enabled objects
and all their dependencies.

* Free software: BSD license

.. warning:: This is highly experimental, it's not guaranteed to work in any
    way, to keep your data intact; it may harm you, your cat and even create a
    black hole in a server near you. You've been warned!


Features
********

Largely based on django ``dump_data`` command it differs in two aspects:

- Objects selection is based on a queryset passed by the user (as string)
- Objects dependencies are evaluated on a per-instance base to dump only the
  corresponding dependent instances.
