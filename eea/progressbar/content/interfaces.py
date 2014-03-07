""" Depiction content interfaces
"""
from zope.interface import Interface

class IProgressTool(Interface):
    """ Local utility to store and customize content-types schema progress
    """

class IContentType(Interface):
    """ Content-type
    """
