from cms.models.fields import PlaceholderField
from django.contrib.contenttypes.models import ContentType
from django.db import models

from .dump_objects import Command as GeneralCommand


class Command(GeneralCommand):
    help = ("Output the contents of the given queryset as a fixture of the given"
            "format (using each model's default manager unless --all is "
            "specified). django CMS enabled version that can dump the plugins"
            "in PlaceholderField")

    def extract_fields(self, item):
        objects = []
        for field in item._meta.fields:
            value = getattr(item, field.name)
            if isinstance(field, models.ForeignKey):
                if value:
                    objects.extend(self.extract_fields(value))
            if isinstance(field, PlaceholderField):
                if value:
                    objects.extend(self.extract_fields(value))
                    for plugin in value.get_plugins_list():
                        objects.extend(self.extract_fields(plugin.get_plugin_instance()[0]))
        if not isinstance(item, ContentType):
            objects.append(item)
        return objects