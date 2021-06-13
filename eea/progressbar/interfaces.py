""" Custom interfaces

    >>> from zope.component import queryAdapter
    >>> from eea.progress.workflow.interfaces import IWorkflowProgress

    >>> portal = layer['portal']
    >>> sandbox = portal._getOb('sandbox')

"""
from zope.interface import Interface
from Products.ZCatalog.interfaces import ICatalogBrain as IZCatalogBrain
from plone.app.collection.interfaces import ICollection as IPloneCollection

# Tool
from eea.progressbar.content.interfaces import IProgressTool
from eea.progressbar.content.interfaces import IContentType

# ControlPanel
from eea.progressbar.controlpanel.interfaces import ISettings

# Storage
from eea.progressbar.storage.interfaces import IStorage

#
# Marker interfaces
#
class IWorkflowTool(Interface):
    """ Marker interface for portal_workflow
    """


class ICollection(IPloneCollection):
    """ Marker interface for plone.app.collection
    """


class ICatalogBrain(IZCatalogBrain):
    """ Marker interface for Catalog Brains
    """

#
# Browser layer
#

class IProgressBarLayer(Interface):
    """ Browser layer for eea.progressbar
    """

__all__ = [
    IProgressTool.__name__,
    IContentType.__name__,
    ISettings.__name__,
    IStorage.__name__,
]
