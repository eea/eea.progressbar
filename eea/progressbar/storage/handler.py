""" Progress storage annotations
"""
from persistent.list import PersistentList
from persistent.dict import PersistentDict
from zope.interface import implements
from zope.annotation.interfaces import IAnnotations
from eea.progressbar.storage.interfaces import IStorage
from eea.progressbar.config import ANNO_FIELDS
ANNO_ORDER = ANNO_FIELDS + u'.order'

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
            fields = anno[ANNO_FIELDS] = PersistentDict()
        return fields

    def _order(self):
        """ Fields order
        """
        anno = IAnnotations(self.context)
        order = anno.get(ANNO_ORDER, None)
        if order is None:
            order = anno[ANNO_ORDER] = PersistentList()
        return order

    @property
    def fields(self):
        """ Fields
        """
        anno = IAnnotations(self.context)
        return anno.get(ANNO_FIELDS, {})

    @property
    def order(self):
        """ Order
        """
        anno = IAnnotations(self.context)
        return anno.get(ANNO_ORDER, [])

    def field(self, name, default=None):
        """ Return field by given key
        """
        return self.fields.get(name, default)

    def add_field(self, name, **kwargs):
        """ Add new field
        """
        if self.field(name):
            raise KeyError(name)

        config = self._fields()
        kwargs.update({'name': name})
        field = PersistentDict(kwargs)
        config[name] = field
        return name

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
        return config.pop(name)

    def delete_fields(self):
        """ Delete all fields
        """
        anno = IAnnotations(self.context)
        anno[ANNO_FIELDS] = PersistentDict()

    def reorder(self, order=()):
        """ Reorder fields
        """
        anno = IAnnotations(self.context)
        anno[ANNO_ORDER] = PersistentList(order)
