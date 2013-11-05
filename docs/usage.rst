=====
Usage
=====

The main feature of `cms_dump_objects` is that you can select data to be exported
using a normal Django QuerySet.

QuerySet must be written in quotes and can only contain scalar value as arguments
to `filter`, `exclude` and other selection methods. Only methods that return a
QuerySet can be used.

It share most other arguments with `dump_data`.

Examples
********

To dump the whole page tree with all the respective plugins and content::

    ./manage.py cms_dump_objects 'cms.Page.objects.all()' > /path/to/dump.json

To dump a branch starting for a given page::

    ./manage.py cms_dump_objects -r 'cms.Page.objects.filter(reverse_id=whatever)' > /path/to/dump.json


Options
*******

* ``--format``: Specifies the output serialization format for fixtures;
  by using Django serializer, you can use any serialization format enabled in
  your project.
* ``--indent``: Specifies the indent level to use when pretty-printing output.
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

Caveats
*******

* As Django ``loaddata`` command matches objects based on their primary key,
  this tool is mostly intended as a way to do partial backup of existing projects,
  and to move data between different instances of the same project (say:
  development and testing environment and so on); using it to move data between
  projects can lead to data overwrite and data loss.

* When exporting a partial subset of pages, all the ancestors will be dumped too,
  to be able to load them back in a project; existing pages with the same
  primary keys in the target project will overwritten.

* To avoid the above behavior use ``-s`` option, but to be able to load data back
  you'll need to have the pages with the needed primary keys before loading.