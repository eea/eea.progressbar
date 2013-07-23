""" Browser controllers
"""
from zope.component import queryAdapter
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from eea.progressbar.interfaces import IWorkflowProgress

class ProgressBarView(BrowserView):
    """ Progress bar
    """
    def __init__(self, context, request):
        super(ProgressBarView, self).__init__(context, request)
        self._info = None
        self._state = None

    @property
    def state(self):
        """ Current state
        """
        if self._state is None:
            wftool = getToolByName(self.context, 'portal_workflow')
            self._state = wftool.getInfoFor(self.context, 'review_state')
        return self._state

    @property
    def info(self):
        """ Get progress for context based on current state
        """
        if self._info is not None:
            return self._info

        wftool = getToolByName(self.context, 'portal_workflow')

        # Look for more specific adapters
        for wf in wftool.getChainFor(self.context):
            info = queryAdapter(self.context, IWorkflowProgress, name=wf)
            if not info:
                continue
            self._info = info
            return self._info

        # Fallback on generic adapter
        self._info = queryAdapter(self.context, IWorkflowProgress)
        return self._info

    @property
    def table(self):
        """ Compute visual progress bar
        """
        current = 0
        for state, progress in self.info.steps:
            width = progress - current
            current = progress
            yield state, progress, width

class CollectionProgressBarView(ProgressBarView):
    """ Progress bar for collections
    """
    @property
    def table(self):
        """ Compute visual progress bar
        """
        info = self.info
        table = [info.closed, info.opened, info.total]
        current = 0
        for index, (state, progress) in enumerate(self.info.steps):
            width = progress - current
            current = progress
            yield state, table[index], width
