""" Progress tool
"""
from zope.interface import implements
from Products.CMFCore.utils import UniqueObject
from Products.ATContentTypes.content.folder import ATFolder
from eea.progressbar.content.interfaces import IProgressTool
from eea.progressbar.content.contenttype import finalize_schema

SCHEMA = ATFolder.schema.copy()
finalize_schema(SCHEMA)

class ProgressTool(UniqueObject, ATFolder):
    """ Local utility to store and customize content-types schema progress
    """
    implements(IProgressTool)

    meta_type = portal_type = 'ProgressTool'
    archetypes_name = 'EEA Progress Bar Tool'
    manage_options = ATFolder.manage_options
    schema = SCHEMA
    _at_rename_after_creation = False

    def get(self, portal_type, default=None):
        """ Get child by portal_type
        """
        for child in self.objectValues():
            field = child.getField('ctype')
            value = field.getAccessor(child)()
            if value == portal_type:
                return child
        return default
