""" Custom interfaces

    >>> from zope.component import queryAdapter
    >>> from eea.progress.workflow.interfaces import IWorkflowProgress

    >>> portal = layer['portal']
    >>> sandbox = portal._getOb('sandbox')

"""
from zope.interface import Interface

# Tool
from eea.progressbar.content.interfaces import IProgressTool
from eea.progressbar.content.interfaces import IContentType

# ControlPanel
from eea.progressbar.controlpanel.interfaces import ISettings

# Storage
from eea.progressbar.storage.interfaces import IStorage

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
