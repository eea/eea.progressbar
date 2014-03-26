""" Storage interfaces

    >>> from zope.component import queryUtility
    >>> from eea.progressbar.interfaces import IProgressTool

"""
from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.annotation.attribute import AttributeAnnotations
from zope.interface import Interface
from eea.progressbar.config import EEAMessageFactory as _

class IStorage(Interface):
    """ Annotations Storage

        >>> ptool = queryUtility(IProgressTool)
        >>> cid = ptool.invokeFactory('ProgressContentType', id='document')
        >>> sandbox = ptool[cid]

        >>> from eea.progressbar.interfaces import IStorage
        >>> storage = IStorage(sandbox)
        >>> storage
        <eea.progressbar.storage.handler.Storage object at ...>

        >>> storage.fields
        {}

        >>> storage.order
        []

    """

    fields = schema.Dict(title=_(u"Custom fields settings"), readonly=True)
    order = schema.List(title=_(u"Custom order of fields"), readonly=True)

    def add_field(name, kwargs):
        """ Add new field configuration

            >>> storage.add_field('title', icon='eea-icon', ready='Title added')
            'title'

            >>> storage.add_field('effectiveDate')
            'effectiveDate'

            >>> storage.add_field('expirationDate')
            'expirationDate'

        """

    def field(name, default):
        """ Get field by given name

            >>> storage.field('description', {})
            {}

            >>> storage.field('title')
            {...'name': 'title'...}

        """

    def edit_field(name, kwargs):
        """ Edit field configuration

            >>> storage.edit_field('description', icon="eea-icon-pencil")
            'description'

            >>> storage.field('description')
            {...'name': 'description'...}

        """

    def delete_field(name):
        """ Delete field configuration

            >>> storage.delete_field('relatedItems')
            Traceback (most recent call last):
            ...
            KeyError: 'relatedItems'

            >>> storage.delete_field('description')
            {...'name': 'description'...}

            >>> 'description' in storage.fields
            False

        """

    def reorder(order):
        """ Reorder fields

            >>> storage.reorder(('effectiveDate', 'expirationDate', 'title'))
            >>> storage.order
            ['effectiveDate', 'expirationDate', 'title']

        """

    def delete_fields():
        """ Delete all fields

            >>> storage.delete_fields()
            >>> storage.fields
            {}

        """


__all__ = [
    IAnnotations.__name__,
    AttributeAnnotations.__name__,
    IStorage.__name__,
]
