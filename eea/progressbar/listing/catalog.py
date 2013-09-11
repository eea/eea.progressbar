""" Catalog
"""
from zope.interface import implements
from zope.component import queryMultiAdapter
from plone.app.contentlisting.catalog import CatalogContentListingObject
from plone.app.contentlisting.interfaces import IContentListingObject

class ProgressCatalogListingObject(CatalogContentListingObject):
    """ Extend Catalog Content listing with progress property
    """
    implements(IContentListingObject)

    @property
    def progress(self):
        """ Get progress for brain
        """
        context = self.getObject()
        request = context.REQUEST
        progress = queryMultiAdapter((context, request), name=u'progress.bar')
        return progress()

    def __getattr__(self, name):
        """ Get progress
        """
        if name == u'progress':
            return self.progress
        return super(ProgressCatalogListingObject, self).__getattr__(name)
