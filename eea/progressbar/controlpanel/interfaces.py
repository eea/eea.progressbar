""" Interfaces
"""
from zope.interface import Interface
from zope import schema
from eea.progressbar.config import EEAMessageFactory as _

class ISettings(Interface):
    """ Alchemy settings
    """
    viewletVisibleFor = schema.List(
        title=_(u"Enable workflow percentage bar viewlet"),
        description=_(u"Workflow percentage bar viewlet is visible for the "
                      u"following content-types"),
        required=False,
        default=[u"Document", u"Collection", u"Folder", u"News Item", u"Event"],
        value_type=schema.Choice(
            vocabulary="plone.app.vocabularies.ReallyUserFriendlyTypes")
    )

    trailViewletVisibleFor = schema.List(
        title=_(u"Enable workflow steps trail viewlet"),
        description=_(u"Workflow steps trail viewlet is visible for the "
                      u"following content-types"),
        required=False,
        default=[u"Document", u"Collection", u"Folder", u"News Item", u"Event"],
        value_type=schema.Choice(
            vocabulary="plone.app.vocabularies.ReallyUserFriendlyTypes")
    )
