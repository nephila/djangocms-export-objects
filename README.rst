===============================
django CMS Export Objects
===============================

.. image:: https://badge.fury.io/py/djangocms-export-objects.png
        :target: http://badge.fury.io/py/djangocms-export-object
    
.. image:: https://travis-ci.org/nephila/djangocms-export-objects.png?branch=master
        :target: https://travis-ci.org/nephila/djangocms-export-objects

.. image:: https://pypip.in/d/djangocms-export-objects/badge.png
        :target: https://crate.io/packages/djangocms-export-objects?version=latest

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

Options valid only when dumping Page objects
--------------------------------------------

* ``-r``, ``--recursive``: it will fetch all the pages whose ancestor is in the
  given queryset (i.e.: it dumps branches of the page tree).
* ``-s``, ``--skip-ancestors``: Skip the ancestors of the pages in the given
  queryset. **Use this at your own risk**: You'll not be able do load back the
  data if you don't have **all** the ancestors of the dumped pages in the
  project you're loading this fixtures to.

Usage
*****

To dump the whole page tree with all the respective plugins and content::

    ./manage.py cms_dump_objects 'cms.Page.objects.all()' > /path/to/dump.json

To dump a branch starting for a given page::

    ./manage.py cms_dump_objects -r 'cms.Page.objects.filter(reverse_id=whatever)' > /path/to/dump.json


Caveats
*******

* As Django ``load_data`` command matches objects based on their primary key,
  this tool is mostly intended as a way to do partial backup of existing projects,
  and to move data between different instances of the same project (say:
  development and testing environment and so on); using it to move data between
  projects can lead to data overwrite and data loss.

* When exporting a partial subset of pages, all the ancestors will be dumped too,
  the be able to load them back in a project; existing pages with the same
  primary keys in the target project will overwritten.

* To avoid the above behavior use ``-s`` option, but to be able to load data back
  you'll need to have the pages with the needed primary keys before loading.