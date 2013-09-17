""" Interfaces
"""
from zope.interface import Interface
from zope import schema
from eea.progressbar.config import EEAMessageFactory as _

class ISettings(Interface):
    """ Alchemy settings
    """
    viewletVisibleFor = schema.List(
        title=_(u"Enable progressbar viewlet"),
        description=_(u"Progressbar viewlet is visible for the "
                      "following content-types"),
        required=False,
        default=[u"Document", u"Collection", u"Folder", u"News Item", u"Event"],
        value_type=schema.Choice(
            vocabulary="plone.app.vocabularies.ReallyUserFriendlyTypes")
    )
