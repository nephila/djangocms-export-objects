# -*- coding: utf-8 -*-
import collections


class InstancesList(collections.OrderedDict):

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
