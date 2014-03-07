""" Progress adapters
"""
from plone.uuid.interfaces import IUUID
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.CMFPlone.utils import base_hasattr
from zope.component import queryAdapter, queryUtility
from zope.interface import implements
from eea.progressbar.controlpanel.interfaces import ISettings
from eea.progressbar.interfaces import IWorkflowProgress, IProgressTool

class WorkflowProgress(object):
    """
    Abstract adapter for workflow progress. This will be used as a fallback
    adapter if the API can't find a more specific adapter for your workflow

    """
    implements(IWorkflowProgress)

    def __init__(self, context):
        self.context = context
        self._hasProgress = None
        self._progress = None
        self._done = None
        self._steps = None
        self._minProgress = None

    @property
    def minProgress(self):
        """ Minimum progress to display
        """
        if not self._minProgress:
            ptool = queryUtility(IProgressTool)
            settings = queryAdapter(ptool, ISettings)
            self._minProgress = settings.hidedStatesPercentage
        return self._minProgress

    @property
    def hasProgress(self):
        """ Is progress updated
        """
        if self._hasProgress is not None:
            return self._hasProgress

        wftool = getToolByName(self.context, 'portal_workflow')
        workflows = wftool.getWorkflowsFor(self.context)
        for wf in workflows:
            for state in wf.states.values():
                progress = (state.progress if base_hasattr(state, 'progress')
                            else None)
                if progress:
                    self._hasProgress = True
                    return self._hasProgress

        self._hasProgress = False
        return self._hasProgress

    def guessProgress(self, state):
        """ Guess progress from state
        """
        if 'private' in state.lower():
            return 33
        elif 'pending' in state.lower():
            return 66
        elif 'published' in state.lower():
            return 100
        elif 'visible' in state.lower():
            return 100
        elif 'internal' in state.lower():
            return 100
        elif 'external' in state.lower():
            return 100
        return 0

    @property
    def progress(self):
        """ Progress
        """
        if self._progress is not None:
            return self._progress

        self._progress = 0
        wftool = getToolByName(self.context, 'portal_workflow')
        try:
            state = wftool.getInfoFor(self.context, 'review_state')
        except WorkflowException:
            state = 'published'

        # No progress defined
        if not self.hasProgress:
            self._progress = self.guessProgress(state)
            return self._progress

        # Progress defined via ZMI
        workflows = wftool.getWorkflowsFor(self.context)
        for wf in workflows:
            state = wf.states.get(state)
            if not state:
                continue
            progress = (state.progress if base_hasattr(state, 'progress')
                        else None)
            if progress is not None:
                self._progress = progress
                break

        return self._progress

    @property
    def done(self):
        """ Done
        """
        return self.progress

    @property
    def steps(self):
        """ Return a SimpleVocabulary like tuple with steps and % done like:

        (
          ('private', 0, 'Private'),
          ('pending': 50, 'Pending'),
          ('visible': 50, 'Public Draft'),
          ('published', 100, 'Public')
        )

        """
        if self._steps is not None:
            return self._steps

        hasProgress = self.hasProgress

        def compare(a, b):
            """ Sort
            """
            a_progress = ((a[1].progress
                           if base_hasattr(a[1], 'progress') else  0) if
                          hasProgress else self.guessProgress(a[0]))
            b_progress = ((b[1].progress
                           if base_hasattr(b[1], 'progress') else 0) if
                          hasProgress else self.guessProgress(b[0]))

            return cmp(a_progress, b_progress)

        self._steps = []
        wftool = getToolByName(self.context, 'portal_workflow')
        progress_steps = {}

        for wf in wftool.getWorkflowsFor(self.context):
            for name, item in sorted(wf.states.items(), cmp=compare):
                title = item.title if base_hasattr(item, 'title') else name
                description = (item.description or title
                    if base_hasattr(item, 'description') else title)
                if hasProgress:
                    progress = (item.progress if
                                base_hasattr(item, 'progress') else 0)
                else:
                    progress = self.guessProgress(name)

                if progress <= self.minProgress:
                    continue

                has_progress = progress_steps.get(progress)

                if has_progress:
                    name_list = has_progress[0]
                    title_list = has_progress[2]
                    desc_list = has_progress[3]

                    name_list.append(name)
                    title_list.append(title)
                    desc_list.append(description)
                else:
                    step = ([name, ], progress, [title, ], [description, ])
                    self._steps.append(step)
                    progress_steps[progress] = step

            break
        return self._steps

class CollectionWorkflowProgress(WorkflowProgress):
    """ Workflow progress used for Collections
    """
    def __init__(self, context):
        super(CollectionWorkflowProgress, self).__init__(context)
        self.total = 0
        self.closed = 0
        self.opened = 0

    @property
    def progress(self):
        """ Progress only closed children (that are 100% done)
        """
        if self._progress is not None:
            return self._progress

        results = getattr(self.context, 'results', None)
        if not results:
            return 0

        progress = 0
        brains = results()
        total = len(brains)

        for brain in brains:
            if getattr(brain, 'getObject', None):
                doc = brain.getObject()
            else:
                doc = brain

            # Avoid recursion errors
            if IUUID(doc) == IUUID(self.context):
                continue

            adapter = queryAdapter(doc, IWorkflowProgress)
            if not adapter:
                continue

            my_progress = adapter.progress
            if my_progress >= 100:
                progress += 1
                self.closed += 1
            else:
                self.opened += 1

        self._progress = 100.0 * progress / (total or 1)
        self.total = total

        return self._progress

    @property
    def done(self):
        """ % Done for all children even if they are not 100% done
        """
        if self._done is not None:
            return self._done

        results = getattr(self.context, 'results', None)
        if not results:
            results = getattr(self.context, 'queryCatalog', None)

        if not results:
            return 0

        progress = 0
        brains = results()
        total = len(brains)

        for brain in brains:
            if getattr(brain, 'getObject', None):
                doc = brain.getObject()
            else:
                doc = brain

            # Avoid recursion errors
            if IUUID(doc) == IUUID(self.context):
                continue

            adapter = queryAdapter(doc, IWorkflowProgress)
            if not adapter:
                continue

            progress += adapter.done

        self._done = progress / (total or 1)
        return self._done
