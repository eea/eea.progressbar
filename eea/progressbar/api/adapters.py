""" Progress adapters
"""
from zope.interface import implements
from zope.component import queryAdapter
from plone.uuid.interfaces import IUUID
from Products.CMFCore.utils import getToolByName
from eea.progressbar.interfaces import IWorkflowProgress

class WorkflowProgress(object):
    """ Abstract adapter for workflow progress. This will be used as a fallback
    adapter if the API can't find a more specific adapter for your workflow
    """
    implements(IWorkflowProgress)

    def __init__(self, context):
        self.context = context
        self._progress = None
        self._done = None
        self._steps = None

    @property
    def progress(self):
        """ Progress
        """
        if self._progress is not None:
            return self._progress

        self._progress = 0
        wftool = getToolByName(self.context, 'portal_workflow')
        state = wftool.getInfoFor(self.context, 'review_state')
        workflows = wftool.getWorkflowsFor(self.context)
        for wf in workflows:
            state = wf.states.get(state)
            if not state:
                continue
            self._progress = getattr(state, 'progress', 0)
        return self._progress

    @property
    def done(self):
        """ Done
        """
        return self.progress

    @property
    def steps(self):
        """ Return a list with steps and % done like:

        [('private', 0), ('pending': 50), ('visible': 50), (published, 100)]

        """
        if self._steps is not None:
            return self._steps

        def compare(a, b):
            """ Sort
            """
            a_progress = getattr(a[1], 'progress', None) or 0
            b_progress = getattr(b[1], 'progress', None) or 0
            return cmp(a_progress, b_progress)

        self._steps = []
        wftool = getToolByName(self.context, 'portal_workflow')
        for wf in wftool.getWorkflowsFor(self.context):
            self._steps = [
                (name, getattr(item, 'progress', 0))
                for name, item in sorted(wf.states.items(), cmp=compare)]
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

    @property
    def steps(self):
        """ Return a list with steps and % done like:

        [('closed', 33), ('done': 63), ('total': 100), (published, 100)]

        """
        return [
            ('closed', self.progress),
            ('done', self.done),
            ('total', 100),
        ]
