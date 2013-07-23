""" Custom interfaces
"""
from zope.interface import Interface
from zope import schema
from eea.progressbar.config import EEAMessageFactory as _
#
# Marker interfaces
#
class IWorkflowTool(Interface):
    """ Marker interface for portal_workflow
    """

class IWorkflow(Interface):
    """ Marker interface for workflow
    """

class IWorkflowState(Interface):
    """ Marker interface for workflow state
    """

class IBaseObject(Interface):
    """ Marker interface for Archetypes or Dexterity objects
    """

class ICollection(Interface):
    """ Marker interface for plone.app.collection and ATTopic
    """
#
# Adapters
#
class IWorkflowProgress(Interface):
    """ These adapters provides progress information for an object
    """
    progress = schema.Int(
        title=_(u"Progress"),
        description=_(u"For a folderish item, this can be the sum of all items"
                      "with progress 100% / total items possible progress"),
        readonly=True,
        default=0
    )

    done = schema.Int(
        title=_(u"% Done"),
        description=_(u"For a folderish item, this can be the sum of all items"
                      "progress / total items possible progress"),
        readonly = True,
        default=0
    )

    steps = schema.List(
        title=_(u"Steps"),
        description=_(u"A list of workflow steps with percetage"),
        readonly=True
    )
