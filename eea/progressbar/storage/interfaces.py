""" Storage interfaces
"""
from zope.annotation.interfaces import IAnnotations
from zope.annotation.attribute import AttributeAnnotations
from zope.interface import Interface

class IStorage(Interface):
    """ Annotations Storage
    """

__all__ = [
    IAnnotations.__name__,
    AttributeAnnotations.__name__,
    IStorage.__name__,
]
