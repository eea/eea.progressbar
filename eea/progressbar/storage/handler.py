""" Progress storage annotations
"""
from persistent.dict import PersistentDict
from persistent.list import PersistentList
from zope.interface import implements
from zope.annotation.interfaces import IAnnotations
from eea.progressbar.storage.interfaces import IStorage
from eea.progressbar.config import ANNO_FIELDS

class Storage(object):
    """ Save/Get progress info
    """
    implements(IStorage)

    def __init__(self, context):
        self.context = context


    def _fields(self):
        """ Fields
        """
        anno = IAnnotations(self.context)
        fields = anno.get(ANNO_FIELDS, None)
        if fields is None:
            fields = anno[ANNO_FIELDS] = PersistentList()
        return fields

    @property
    def fields(self):
        """ Fields
        """
        anno = IAnnotations(self.context)
        return anno.get(ANNO_FIELDS, [])

    def field(self, name, default=None):
        """ Return field by given key
        """
        for field in self.fields:
            if field.get('name', '') != name:
                continue
            return field
        return default

    def add_field(self, name, **kwargs):
        """ Add new field
        """
        if self.field(name):
            raise KeyError(name)

        config = self._fields()
        kwargs.update({'name': name})
        field = PersistentDict(kwargs)
        config.append(field)
        return field.get('name', '')

    def edit_field(self, name, **kwargs):
        """ Edit field properties
        """
        field = self.field(name)
        if not field:
            return self.add_field(name, **kwargs)
        return field.update(kwargs)

    def delete_field(self, name):
        """ Delete field by given name
        """
        config = self._fields()
        for index, field in enumerate(config):
            if field.get('name', '') == name:
                config.pop(index)
                return name
        raise KeyError(name)

    def delete_fields(self):
        """ Delete all fields
        """
        anno = IAnnotations(self.context)
        anno[ANNO_FIELDS] = PersistentList()
