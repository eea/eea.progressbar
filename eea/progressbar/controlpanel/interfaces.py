""" Control Panel Interfaces

    >>> from zope.component import queryUtility, queryAdapter
    >>> from eea.progressbar.interfaces import IProgressTool
    >>> from eea.progressbar.interfaces import ISettings

"""
from zope.interface import Interface
from zope import schema
from eea.progressbar.config import EEAMessageFactory as _

class ISettings(Interface):
    """ Alchemy settings

        >>> ptool = queryUtility(IProgressTool)
        >>> settings = queryAdapter(ptool, ISettings)
        >>> settings
        <eea.progressbar.controlpanel.settings.ControlPanelAdapter object at...>

        >>> settings.viewletVisibleFor
        [u'Document', u'Collection', u'Folder', u'News Item', u'Event']

        >>> settings.viewletVisibleFor = [u'Folder']
        >>> settings.viewletVisibleFor
        [u'Folder']

        >>> settings.trailViewletVisibleFor
        [u'Document', u'Collection', u'Folder', u'News Item', u'Event']

        >>> settings.trailViewletVisibleFor = [u'Document']
        >>> settings.trailViewletVisibleFor
        [u'Document']

        >>> settings.metadataViewletVisibleFor
        []

        >>> settings.metadataViewletVisibleFor = [u'Event']
        >>> settings.metadataViewletVisibleFor
        [u'Event']

        >>> settings.hidedStatesPercentage
        0

        >>> settings.hidedStatesPercentage = -1
        >>> settings.hidedStatesPercentage
        -1

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

    metadataViewletVisibleFor = schema.List(
        title=_(u"Enable editing progress viewlet"),
        description=_(u"Editing progress viewlet is visible for the "
                      u"following content-types"),
        required=False,
        default=[],
        value_type=schema.Choice(
            vocabulary="plone.app.vocabularies.ReallyUserFriendlyTypes")
    )

    hidedStatesPercentage = schema.Int(
        title=_(u"Ignore states lower than or equal to"),
        description=_(u"Ignore states that have a "
                      u"defined percentage lower than or equal to"),
        required=False,
        default=0
    )
