djangocms-export-objects
========================

A django CMS command to export PlaceholderFields-enable objects and all their
dependencies.

Largely base on django ``dump_data`` command it differs in two aspects:

 - Objects selection is based on a queryset passed by the user (as string)
 - Objects dependencies are evaluated on a per-instance base to dump only the
   corresponding dependent instances.
