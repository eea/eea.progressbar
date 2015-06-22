""" Custom content-types
"""
from Products.CMFCore import utils as cmfutils
from Products.Archetypes.atapi import process_types, listTypes
from eea.progressbar.config import (
    PROJECTNAME,
    ADD_CONTENT_PERMISSION
)

from Products.Archetypes.atapi import registerType
from eea.progressbar.content.tool import ProgressTool
from eea.progressbar.content.contenttype import ProgressContentType

registerType(ProgressTool, PROJECTNAME)
registerType(ProgressContentType, PROJECTNAME)

def initialize(context):
    """ Zope 2
    """
    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    cmfutils.ToolInit(PROJECTNAME+' Tools',
                tools=[ProgressTool],
                icon='content/tool.png'
                ).initialize(context)

    cmfutils.ContentInit(
        PROJECTNAME + ' Content',
        content_types=content_types,
        permission=ADD_CONTENT_PERMISSION,
        extra_constructors=constructors,
        fti=ftis,
        ).initialize(context)
