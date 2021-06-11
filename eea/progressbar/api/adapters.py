""" Progress adapters
"""
from plone.uuid.interfaces import IUUID
from zope.component import queryAdapter
from eea.progress.workflow.interfaces import IWorkflowProgress
from eea.progress.workflow.api.adapters import WorkflowProgress


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
