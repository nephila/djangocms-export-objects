# -*- coding: utf-8 -*-
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict


class InstancesList(OrderedDict):

    def get_model_path(self, elem):
        return "%s.%s" % (elem._meta.app_label, elem._meta.module_name)

    def get_label(self, elem):
        return "%s.%s.%s" % (elem._meta.app_label, elem._meta.module_name, elem.pk)

    def update(self, *args, **kwargs):
        if kwargs:
            raise TypeError("update() takes no keyword arguments")

        for s in args:
            for e in s:
                 self.add(e)

    def add(self, elem):
        label = self.get_label(elem)
        if not label in self:
            self[label] = elem

    def model_list(self):
        app_list = OrderedDict()
        for item in self.values():
            app, model = item._meta.app_label, item.__class__
            if app not in app_list:
                app_list[app] = []
            app_list[app].append(model)
        return app_list

    def get_items_by_model_path(self, model):
        path = "%s" % (model._meta)
        items = []
        for label, item in self.items():
            if label.startswith(path):
                items.append(item)
        return items

    def discard(self, elem):
        self.pop(elem, None)

    def __le__(self, other):
        return all(e in other.keys() for e in self.keys())

    def __lt__(self, other):
        return self.keys() <= other.keys() and self.keys() != other.keys()

    def __ge__(self, other):
        return all(e in self.keys() for e in other.keys())

    def __gt__(self, other):
        return self.keys() >= other.keys() and self.keys() != other.keys()

    def __repr__(self):
        return 'InstancesList([%s])' % (', '.join(map(repr, self.keys())))

    def __str__(self):
        return '{%s}' % (', '.join(map(repr, self.keys())))
