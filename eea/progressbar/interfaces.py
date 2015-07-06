""" Custom interfaces

    >>> from zope.component import queryAdapter
    >>> from eea.progressbar.interfaces import IWorkflowProgress

    >>> portal = layer['portal']
    >>> sandbox = portal._getOb('sandbox')

"""
from zope.interface import Interface
from zope import schema
from Products.ZCatalog.interfaces import ICatalogBrain as IZCatalogBrain
from eea.progressbar.config import EEAMessageFactory as _
from plone.app.collection.interfaces import ICollection as IPloneCollection

# Tool
from eea.progressbar.content.interfaces import IProgressTool
from eea.progressbar.content.interfaces import IContentType

# ControlPanel
from eea.progressbar.controlpanel.interfaces import ISettings

# Storage
from eea.progressbar.storage.interfaces import IStorage

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

class ICollection(IPloneCollection):
    """ Marker interface for plone.app.collection
    """

class ICatalogBrain(IZCatalogBrain):
    """ Marker interface for Catalog Brains
    """
#
# Browser layer
#
class IProgressBarLayer(Interface):
    """ Browser layer for eea.progressbar
    """

#
# Adapters
#
class IWorkflowProgress(Interface):
    """
    These adapters provides progress information for an object

    By default, if you don't manually define any progress via ZMI
    the system tries to guess the progress using a very simple algorithm:

      - private = 33%
      - pending = 66%
      - published = 100%


        >>> IWorkflowProgress(sandbox).hasProgress
        False

        >>> IWorkflowProgress(sandbox).progress
        33

        >>> portal.portal_workflow.doActionFor(sandbox, 'submit')
        >>> IWorkflowProgress(sandbox).progress
        66

        >>> portal.portal_workflow.doActionFor(sandbox, 'publish')
        >>> IWorkflowProgress(sandbox).progress
        100

    You can also get a list of steps and their percentage:


        >>> IWorkflowProgress(sandbox).steps
        [(['private'], 33, ['Private'], ...(['published'], 100, ['Publish...)]

    And % done (on a simple item it's the same as progress). This is useful
    within Collections

        >>> IWorkflowProgress(sandbox).done
        100

    You can always change progress values per state via ZMI:

        >>> wf = portal.portal_workflow.simple_publication_workflow
        >>> wf.states.pending.progress = 60
        >>> wf.states.published.progress = 90

        >>> IWorkflowProgress(sandbox).hasProgress
        True

        >>> IWorkflowProgress(sandbox).progress
        90

    Changing at least one state will disable the auto-detection mechanism. So
    don't forget to manually set progress for all possible states within your
    workflow:

        >>> portal.portal_workflow.doActionFor(sandbox, 'retract')
        >>> IWorkflowProgress(sandbox).progress
        0

        >>> portal.portal_workflow.doActionFor(sandbox, 'submit')
        >>> IWorkflowProgress(sandbox).progress
        60

        >>> IWorkflowProgress(sandbox).done
        60

        >>> IWorkflowProgress(sandbox).steps
        [(['pending'], 60, ['Pending revi... (['published'], 90, ['Publi...)]

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
        readonly=True,
        default=0
    )

    steps = schema.List(
        title=_(u"Steps"),
        description=_(u"A list of workflow steps with percetage"),
        readonly=True
    )


__all__ = [
    IProgressTool.__name__,
    IContentType.__name__,
    ISettings.__name__,
    IStorage.__name__,
]
