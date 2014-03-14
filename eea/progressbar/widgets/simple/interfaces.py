""" Simple widget edit schema
"""
from zope import schema
from zope.interface import Interface
from eea.progressbar.widgets.interfaces import IProgressWidgetEdit
from eea.progressbar.config import EEAMessageFactory as _

class ISimpleWidgetEdit(IProgressWidgetEdit):
    """ Simple widget
    """
    labelEmpty = schema.TextLine(
        title=_(u'Message (not set)'),
        description=_(u'Message to be used when property is NOT filled'),
        required=False,
        default=u"Please set the {0} for this item"
    )

    labelReady = schema.TextLine(
        title=_(u'Message (ready)'),
        description=_(u'Message to be used when property is filled'),
        required=False,
        default=u"You added the {0}"
    )

    iconEmpty = schema.TextLine(
        title=_(u'Icon (not set)'),
        description=_(u'Icon to be used when property is NOT filled'),
        required=False,
        default=u'eea-icon eea-icon-check-circle-o eea-icon-2x'
    )

    iconReady = schema.TextLine(
        title=_(u"Icon (ready)"),
        description=_(u"Icon to be used when property is filled"),
        required=False,
        default=u'eea-icon eea-icon-check eea-icon-2x'
    )

    link = schema.TextLine(
        title=_(u'Edit link'),
        description=_(u'Link where to edit this property'),
        default=u'edit#fieldsetlegend-default'
    )

    linkLabel = schema.TextLine(
        title=_(u'Edit link label'),
        description=_(u'Human readable label for edit link'),
        default=u'Add {0}'
    )

    states = schema.List(
        title=_(u'Workflow states'),
        description=_(u"Select workflow states where this will be visible"),
        required=False,
        default=[u'all'],
        value_type=schema.Choice(
            vocabulary=u"eea.progressbar.vocabulary.WorkflowStates")
    )
