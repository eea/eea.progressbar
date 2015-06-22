""" Browser controllers
"""
from zope.component import queryAdapter, queryUtility, queryMultiAdapter
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from eea.progressbar.interfaces import IWorkflowProgress, IProgressTool
from eea.progressbar.config import EEAMessageFactory as _

class ProgressBarView(BrowserView):
    """ Progress bar
    """
    def __init__(self, context, request):
        super(ProgressBarView, self).__init__(context, request)
        self._info = None
        self._state = None
        self._state_title = None

    @property
    def state(self):
        """ Current state
        """
        if self._state is None:
            wftool = getToolByName(self.context, 'portal_workflow')
            self._state = wftool.getInfoFor(self.context, 'review_state')
        return self._state

    @property
    def state_title(self):
        """ Current state title
        """
        if self._state_title is None:
            wftool = getToolByName(self.context, 'portal_workflow')
            self._state_title = wftool.getTitleForStateOnType(
                self.state, self.context.portal_type)
        return self._state_title

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
        for term in self.info.steps:
            state = term[0]
            progress = term[1]
            title = term[2]
            description = term[3]
            width = progress - current
            current = progress
            yield state, progress, width, title, description


class ProgressTrailView(ProgressBarView):
    """ Workflow state trail
    """
    @property
    def table(self):
        """ Compute visual progress bar
        """
        length = len(self.info.steps)
        width = 100 / length
        for term in self.info.steps:
            state = term[0]
            progress = term[1]
            title = term[2]
            description = term[3]
            yield state, progress, width, title, description


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
        for index, term in enumerate(self.info.steps):
            progress = term[1]
            state = term[0]
            title = term[2]
            width = progress - current
            current = progress
            yield state, table[index], width, title


    @property
    def state_title(self):
        """ Current state title
        """
        return _('Total progress')

class ProgressMetadataView(BrowserView):
    """ Editing progress
    """
    def __init__(self, context, request):
        super(ProgressMetadataView, self).__init__(context, request)
        self._ready = 0
        self._total = 0

    @property
    def progress(self):
        """ % done
        """
        if self._total:
            return int((1.0 * self._ready / self._total) * 100)
        return 100

    def schema(self):
        """ Schema
        """
        tool = queryUtility(IProgressTool)
        ctype = getattr(self.context, 'portal_type', '')
        ctype = tool.get(ctype)
        if not ctype:
            return

        wftool = getToolByName(self.context, 'portal_workflow')
        state = wftool.getInfoFor(self.context, 'review_state')
        self.request.ctx = self.context
        config = queryMultiAdapter((ctype, self.request), name=u'view')
        for field in config.schema():
            widget = config.view(field)
            states = [term.value for term in widget.workflow()]
            if u'all' not in states:
                if state not in states:
                    continue

            ready = widget.ready(self.context)
            if ready:
                self._ready += 1

            self._total += 1
            if ready and widget.get('hideReady', False):
                continue

            yield widget
