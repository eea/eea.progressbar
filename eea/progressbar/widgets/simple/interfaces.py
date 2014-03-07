""" Simple widget edit schema
"""
from zope import schema
from zope.interface import Interface
from eea.progressbar.widgets.interfaces import IProgressWidget
from eea.progressbar.config import EEAMessageFactory as _

class ISimpleWidget(IProgressWidget):
    """ Simple widget
    """
    title = schema.TextLine(
        title=_(u'Title'),
        required=False
    )

    iconEmpty = schema.TextLine(
        title=_(u'Icon (not set)'),
        description=_(u'Icon to be used when property is NOT filled'),
        required=False,
        default='eea-icon eea-icon-check-circle-o eea-icon-2x'
    )

    iconReady = schema.TextLine(
        title=_(u"Icon (ready)"),
        description=_(u"Icon to be used when property is filled"),
        required=False,
        default='eea-icon eea-icon-check eea-icon-2x'
    )

    link = schema.TextLine(
        title=_(u'Edit'),
        description=_(u'Link where to edit this property'),
        default=u'edit#fieldsetlegend-default'
    )
