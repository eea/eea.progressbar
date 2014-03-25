""" EEA Relations Content Type
"""
from zope.interface import implements
from Products.Archetypes import atapi
from Products.ATContentTypes.content.folder import ATFolder

from eea.progressbar.content.interfaces import IContentType
from eea.progressbar.config import EEAMessageFactory as _

EditSchema = ATFolder.schema.copy() + atapi.Schema((
    atapi.StringField('ctype',
        schemata="default",
        vocabulary_factory='plone.app.vocabularies.ReallyUserFriendlyTypes',
        required=True,
        widget=atapi.SelectionWidget(
            label=_('Portal type'),
            description=_('Select portal type'),
            i18n_domain="eea"
        )
    ),
))

EditSchema['description'].widget.modes = ()

class ProgressContentType(ATFolder):
    """ Progress node
    """
    implements(IContentType)
    portal_type = meta_type = 'ProgressContentType'
    archetypes_name = 'EEA ProgressBar Content Type'
    _at_rename_after_creation = True
    schema = EditSchema
