# -*- coding: utf-8 -*-
from optparse import make_option
from distutils.version import LooseVersion

from django.db import models, DEFAULT_DB_ALIAS
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand, CommandError
from django.core.management.commands.dumpdata import sort_dependencies
from django.core import serializers
from django.contrib.contenttypes.models import ContentType
from django.utils.datastructures import SortedDict

from ...utils import InstancesList

import cms
from cms.models import Page
from cms.models.fields import PlaceholderField

DJANGOCMS_2 = LooseVersion(cms.__version__) < LooseVersion('3')
DJANGOCMS_2_3 = LooseVersion(cms.__version__) < LooseVersion('2.4')


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--format', default='json', dest='format',
                    help='Specifies the output serialization format for fixtures.'),
        make_option('--indent', default=None, dest='indent', type='int',
                    help='Specifies the indent level to use when pretty-printing output'),
        make_option('--database', action='store', dest='database',
                    default=DEFAULT_DB_ALIAS, help='Nominates a specific database to dump '
                    'fixtures from. Defaults to the "default" database.'),
        make_option('-n', '--natural', action='store_true',
                    dest='use_natural_keys', default=False,
                    help='Use natural keys if they are available.'),
        make_option('-a', '--all', action='store_true', dest='use_base_manager',
                    default=False,
                    help="Use Django's base manager to dump all models stored in the database, including those that would otherwise be filtered or modified by a custom manager."),
        make_option('-r', '--recursive', dest='recursive', action='store_true',
                    default=False,
                    help='Dump all the pages whose ancestor is in the given queryset.'),
        make_option('-s', '--skip-ancestors', dest='skip_ancestors', action='store_true',
                    default=False,
                    help='Dump all the ancestors of the pages in the given queryset.'),
        make_option('-x', '--exclude-models', dest='excluded', action='store',
                    default="",
                    help='Exclude the given models (as strings) from the export.'),
    )
    help = ("Output the contents of the given queryset as a fixture of the given"
            "format (using each model's default manager unless --all is "
            "specified). django CMS enabled version that can dump the plugins"
            "in PlaceholderField")

    args = '[appname.ModelName.objects.filter(...)]'

    dump_list = InstancesList()
    options = {}
    app_labels = []
    _querysets = SortedDict()

    def get_querysets(self):
        from django.db.models import get_app, get_apps, get_model

        if not self._querysets:
            app_list = SortedDict()
            for label in self.app_labels:
                app_label, _, model_qs = label.partition('.')
                try:
                    app = get_app(app_label)
                except ImproperlyConfigured:
                    raise CommandError("Unknown application: %s" % app_label)
                model_label, _, given_qs = model_qs.partition('.')
                # this ensures that model exists and thus the eval'ed string
                # (if valid) is at least a method of the model default manager.
                model = get_model(app_label, model_label)
                if model is None:
                    raise CommandError("Unknown model: %s.%s" % (app_label, model_label))
                if model == Page:
                    qs = []
                    temp_qs = eval("model._default_manager.using('%s').%s" % (
                        self.options.get('database'), given_qs.partition('.')[2]))
                    if self.options.get('recursive'):
                        for page in temp_qs:
                            qs.extend(page.get_descendants(include_self=True))
                    else:
                        qs = temp_qs
                else:
                    if self.options.get('use_base_manager'):
                        qs = eval("model._base_manager.using('%s').%s" % (
                            self.options.get('database'), given_qs.partition('.')[2]))
                    else:
                        qs = eval("model._default_manager.using('%s').%s" % (
                            self.options.get('database'), given_qs.partition('.')[2]))
                if app in app_list.keys():
                    if app_list[app] and model not in app_list[app]:
                        app_list[app].extend(qs)
                else:
                    app_list[app] = qs
            self._querysets = app_list.values()
        return self._querysets

    def handle(self, *app_labels, **options):
        self.options = options
        self.app_labels = app_labels
        self.relateds = []

        format = self.options.get('format')
        indent = self.options.get('indent')
        show_traceback = self.options.get('traceback')
        use_natural_keys = self.options.get('use_natural_keys')
        self.excluded = self.options.get('excluded').split(',')

        # Check that the serialization format exists; this is a shortcut to
        # avoid collating all the objects and _then_ failing.
        if format not in serializers.get_public_serializer_formats():
            raise CommandError("Unknown serialization format: %s" % format)

        try:
            serializers.get_serializer(format)
        except KeyError:
            raise CommandError("Unknown serialization format: %s" % format)

        # Now collate the objects to be serialized.
        self.dump_list = InstancesList()
        for qs in self.get_querysets():
            for item in qs:
                self.extract_fields(item)
        app_list = self.dump_list.model_list()
        obj_list = []
        ordered = sort_dependencies(app_list.items())
        explored = []
        for item in ordered:
            if item not in explored:
                app_list = self.dump_list.get_items_by_model_path(item)
                obj_list.extend(app_list)
                explored.append(item)
        try:
            return serializers.serialize(format, obj_list,
                                         indent=indent,
                                         use_natural_keys=use_natural_keys)
        except Exception, e:
            if show_traceback:
                raise
            raise CommandError("Unable to serialize database: %s" % e)

    def append_item(self, item):
        if (item and
                not self.dump_list.get_model_path(item) in self.excluded and
                not self.dump_list.get_label(item) in self.dump_list and
                not isinstance(item, ContentType)):
            self.dump_list.add(item)

    def extract_fields(self, item):
        if (item and
                not self.dump_list.get_model_path(item) in self.excluded and
                not self.dump_list.get_label(item) in self.dump_list and
                not isinstance(item, ContentType)):
            for field in item._meta.many_to_many:
                value = getattr(item, field.name)
                if isinstance(field, models.ManyToManyField):
                    if value:
                        for related_instance in value.all():
                            if related_instance not in self.relateds:
                                self.relateds.append(related_instance)
                                self.extract_fields(related_instance)
                                self.append_item(related_instance)
            for field in item._meta.fields:
                if (isinstance(item, Page)
                    and self.options.get('skip_ancestors')
                    and field.name == 'parent'):
                        continue
                value = getattr(item, field.name)
                if isinstance(field, models.ForeignKey):
                    if value and value not in self.relateds:
                        self.relateds.append(value)
                        self.extract_fields(value)
                        self.append_item(value)
                if isinstance(field, PlaceholderField):
                    if value:
                        self.extract_fields(value)
                        for plugin in value.get_plugins_list():
                            self.extract_fields(plugin.get_plugin_instance()[0])
            if isinstance(item, Page):
                if DJANGOCMS_2_3:
                    pages = (item, )
                else:
                    pages = (item.get_draft_object(), item.get_public_object())
                for page in pages:
                    for placeholder in page.placeholders.all():
                        self.dump_list.add(placeholder)
                        for plugin in placeholder.get_plugins_list():
                            inst, cls = plugin.get_plugin_instance()
                            if inst:
                                self.extract_fields(inst)
                    self.dump_list.add(page)
                    self.dump_list.update(page.title_set.all())
            else:
                self.append_item(item)