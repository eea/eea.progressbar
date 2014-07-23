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

SCHEMA = ATFolder.schema.copy() + EditSchema.copy()

def finalize_schema(schema=SCHEMA):
    """ Update schema
    """
    for field in schema.fields():
        field.write_permission = 'Manage portal'
        if field.schemata != 'default':
            field.required = False
            field.mode = 'r'

finalize_schema()

class ProgressContentType(ATFolder):
    """ Progress node
    """
    implements(IContentType)
    portal_type = meta_type = 'ProgressContentType'
    archetypes_name = 'EEA ProgressBar Content Type'
    _at_rename_after_creation = True
    schema = SCHEMA
    schema['description'].widget.modes = ()
