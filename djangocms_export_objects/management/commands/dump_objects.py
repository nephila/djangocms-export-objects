from cms.models.fields import PlaceholderField
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand, CommandError
from django.core import serializers
from django.db import models, router, DEFAULT_DB_ALIAS
from django.utils.datastructures import SortedDict

from optparse import make_option

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--format', default='json', dest='format',
            help='Specifies the output serialization format for fixtures.'),
        make_option('--indent', default=None, dest='indent', type='int',
            help='Specifies the indent level to use when pretty-printing output'),
        make_option('--database', action='store', dest='database',
            default=DEFAULT_DB_ALIAS, help='Nominates a specific database to dump '
                'fixtures from. Defaults to the "default" database.'),
        make_option('-n', '--natural', action='store_true', dest='use_natural_keys', default=False,
            help='Use natural keys if they are available.'),
        make_option('-a', '--all', action='store_true', dest='use_base_manager', default=False,
            help="Use Django's base manager to dump all models stored in the database, including those that would otherwise be filtered or modified by a custom manager."),
    )
    help = ("Output the contents of the given queryset as a fixture of the given "
            "format (using each model's default manager unless --all is "
            "specified).")
    args = '[appname.ModelName.objects.filter(...)]'

    def handle(self, *app_labels, **options):
        from django.db.models import get_app, get_apps, get_model

        format = options.get('format')
        indent = options.get('indent')
        using = options.get('database')
        show_traceback = options.get('traceback')
        use_natural_keys = options.get('use_natural_keys')
        use_base_manager = options.get('use_base_manager')

        app_list = SortedDict()
        for label in app_labels:
            app_label, _, model_qs = label.partition('.')
            try:
                app = get_app(app_label)
            except ImproperlyConfigured:
                raise CommandError("Unknown application: %s" % app_label)
            model_label, _, qs = model_qs.partition('.')
            # this ensures that model exists and thus the eval'ed string
            # (if valid) is at least a method of the model default manager.
            model = get_model(app_label, model_label)
            if model is None:
                raise CommandError("Unknown model: %s.%s" % (app_label, model_label))
            if use_base_manager:
                qs = eval("model._base_manager.using('%s').%s" % (
                    using, qs.partition('.')[2]))
            else:
                qs = eval("model._default_manager.using('%s').%s" % (
                    using, qs.partition('.')[2]))
            if app in app_list.keys():
                if app_list[app] and model not in app_list[app]:
                    app_list[app].extend(qs)
            else:
                app_list[app] = qs

        # Check that the serialization format exists; this is a shortcut to
        # avoid collating all the objects and _then_ failing.
        if format not in serializers.get_public_serializer_formats():
            raise CommandError("Unknown serialization format: %s" % format)

        try:
            serializers.get_serializer(format)
        except KeyError:
            raise CommandError("Unknown serialization format: %s" % format)

        # Now collate the objects to be serialized.
        objects = []
        querysets = app_list.values()
        for qs in querysets:
            for item in qs:
                objects.extend(self.extract_fields(item))

        try:
            return serializers.serialize(format, objects, indent=indent,
                                         use_natural_keys=use_natural_keys)
        except Exception, e:
            if show_traceback:
                raise
            raise CommandError("Unable to serialize database: %s" % e)

    def extract_fields(self, item):
        objects = []
        for field in item._meta.fields:
            value = getattr(item, field.name)
            if isinstance(field, models.ForeignKey):
                if value:
                    objects.extend(self.extract_fields(value))
            if isinstance(field, models.ManyToManyField):
                if value:
                    objects.extend(self.extract_fields(value))
        if not isinstance(item, ContentType):
            objects.append(item)
        return objects