""" EEA Relations Content Type
"""
from zope.interface import implements
from Products.Archetypes import atapi
from Products.ATContentTypes.content.folder import ATFolder

from eea.progressbar.content.interfaces import IContentType
from eea.progressbar.config import EEAMessageFactory as _

EditSchema = atapi.Schema((
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

class ProgressContentType(ATFolder):
    """ Progress node
    """
    implements(IContentType)
    portal_type = meta_type = 'ProgressContentType'
    archetypes_name = 'EEA ProgressBar Content Type'
    _at_rename_after_creation = True
    schema = ATFolder.schema.copy() + EditSchema.copy()
    schema['description'].widget.modes = ()
