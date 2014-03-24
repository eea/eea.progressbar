""" Schema extender for Disable Autolinks for context/page
"""
from zope.interface import implements
from zope.component import queryAdapter, queryUtility
from Products.Archetypes.public import BooleanField, BooleanWidget
from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.field import ExtensionField
from eea.progressbar.config import EEAMessageFactory as _
from eea.progressbar.interfaces import IProgressBarLayer, IProgressTool
from eea.progressbar.controlpanel.interfaces import ISettings

class EEABooleanField(ExtensionField, BooleanField):
    """ BooleanField for schema extender
    """

class EEASchemaExtender(object):
    """ Schema extender for progress bar fields
    """
    implements(ISchemaExtender, IBrowserLayerAwareExtender)
    layer = IProgressBarLayer

    fieldsProgress = (
        EEABooleanField(
            name='disableProgressBarViewlet',
            schemata='settings',
            default=False,
            searchable=False,
            widget=BooleanWidget(
                label=_('Hide Workflow Percentage Bar Viewlet'),
                description=_('Hide Workflow Percentage Bar viewlet for '
                              'this context/page'),
            )
        ),
    )

    fieldsTrail = (
        EEABooleanField(
            name='disableProgressTrailViewlet',
            schemata='settings',
            default=False,
            searchable=False,
            widget=BooleanWidget(
                label=_('Hide Workflow Steps Trail Viewlet'),
                description=_('Hide Workflow Steps Trail viewlet for '
                              'this context/page'),
            )
        ),
    )

    fieldsMetadata = (
        EEABooleanField(
            name='disableMetadataViewletVisibleFor',
            schemata='settings',
            default=False,
            searchable=False,
            widget=BooleanWidget(
                label=_('Hide Editing Progress Viewlet'),
                description=_('Hide Editing Progress viewlet for '
                              'this context/page'),
            )
        ),
    )

    def __init__(self, context):
        self.context = context

    def getFields(self):
        """ Returns provenance list field
        """
        ptool = queryUtility(IProgressTool)
        settings = queryAdapter(ptool, ISettings)
        ctype = getattr(self.context, 'portal_type', '')
        fields = ()

        if not settings:
            return  fields

        allowed = settings.viewletVisibleFor or []
        if ctype in allowed:
            fields += self.fieldsProgress

        allowed = settings.trailViewletVisibleFor or []
        if ctype in allowed:
            fields += self.fieldsTrail

        allowed = settings.metadataViewletVisibleFor or []
        if ctype in allowed:
            fields += self.fieldsMetadata

        return fields
