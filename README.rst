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

Options
*******

* ``--format``: Specifies the output serialization format for fixtures;
  by using Django serializer, you can use any serialization format enabled in
  your project.
* ``--indent``: Specifies the indent level to use when pretty-printing output.
* ``--database``: Nominates a specific database to dump fixtures from.
  Defaults to the "default" database. Works in the same way as the ``dump_data``
  option
* ``-n``, ``--natural``: Use natural keys if they are available.
* ``-a``, ``--all``: Use Django's base manager to dump all models stored in the
  database, including those that would otherwise be filtered or modified by a
  custom manager. When dumping ``Page`` objects, ``PageManager`` is always used.
* ``-r``, ``--recursive``: This option only affects ``Page`` objects dump; it
  will fetch all the pages whose ancestor is in the given queryset (i.e.: it
  dumps branches of the page tree).
* ``-s``, ``--skip-ancestors``: Skip the ancestors of the pages in the given
  queryset. **Use this at your own risk**: You'll not be able do load back the
  data if you don't have **all** the ancestors of the dumped pages in the
  project you're loading this fixtures to.

Usage
*****



Caveats
*******

