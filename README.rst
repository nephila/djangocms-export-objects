===============================
django CMS Export Objects
===============================

.. image:: https://badge.fury.io/py/djangocms_export_objects.png
    :target: http://badge.fury.io/py/djangocms_export_objects
    
.. image:: https://travis-ci.org/nephila/djangocms_export_objects.png?branch=master
        :target: https://travis-ci.org/nephila/djangocms_export_objects

.. image:: https://pypip.in/d/djangocms_export_objects/badge.png
        :target: https://crate.io/packages/djangocms_export_objects?version=latest


A django CMS command to export cMS Pages and PlaceholderFields-enabled objects
and all their dependencies.

* Free software: BSD license

.. warning:: This is highly experimental, it's not guaranteed to work in any
    way, to keep your data intact and to not create a black hole in a server
    near you.


Features
********

Largely based on django ``dump_data`` command it differs in two aspects:

 - Objects selection is based on a queryset passed by the user (as string)
 - Objects dependencies are evaluated on a per-instance base to dump only the
   corresponding dependent instances.

Caveats
*******

