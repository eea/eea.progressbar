""" Simple widget edit schema
"""
from zope import schema
from eea.progressbar.widgets.interfaces import IProgressWidgetView
from eea.progressbar.widgets.interfaces import IProgressWidgetEdit
from eea.progressbar.config import EEAMessageFactory as _

class ISimpleWidgetView(IProgressWidgetView):
    """ Simple widget view
    """

    def workflow():
        """ Human readable workflow states
        """

    def condition(context):
        """ Condition to establish if widget state is ready or not
        """


class ISimpleWidgetEdit(IProgressWidgetEdit):
    """ Simple widget edit
    """
    labelEmpty = schema.Text(
        title=_(u'Message (not set)'),
        description=_(u'Message to be used when property is NOT filled'),
        required=False,
        default=u"Please set the {label} of this {context.portal_type}"
    )

    labelReady = schema.Text(
        title=_(u'Message (ready)'),
        description=_(u'Message to be used when property is filled'),
        required=False,
        default=u"You added the {label}"
    )

    iconEmpty = schema.TextLine(
        title=_(u'Icon (not set)'),
        description=_(u'Icon to be used when property is NOT filled'),
        required=False,
        default=u'eea-icon eea-icon-edit'
    )

    iconReady = schema.TextLine(
        title=_(u"Icon (ready)"),
        description=_(u"Icon to be used when property is filled"),
        required=False,
        default=u'eea-icon eea-icon-check'
    )

    link = schema.Text(
        title=_(u'Edit link'),
        description=_(u'Link where to edit this property'),
        required=False,
        default=u'edit#fieldsetlegend-default'
    )

    linkLabel = schema.Text(
        title=_(u'Edit link label'),
        description=_(u'Human readable label for edit link'),
        required=False,
        default=u'Add {label}'
    )

    condition = schema.Text(
        title=_(u'Condition (ready)'),
        description=_(u"Tal condition to mark this as ready"),
        required=False,
        default=u"python:value"
    )

    hideReady = schema.Bool(
        title=_(u'Hide (ready)'),
        description=_(u"Hide this if it's ready (completed)"),
        required=False,
        default=False
    )

    states = schema.List(
        title=_(u'Workflow states'),
        description=_(u"Select workflow states where this will be visible"),
        required=False,
        default=[u'all'],
        value_type=schema.Choice(
            vocabulary=u"eea.progressbar.vocabulary.WorkflowStates")
    )
