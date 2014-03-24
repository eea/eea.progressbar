""" Custom viewlets
"""
from zope.component import queryMultiAdapter, queryAdapter, queryUtility
from plone.app.layout.viewlets import common
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from eea.progressbar.controlpanel.interfaces import ISettings
from eea.progressbar.interfaces import IProgressTool


class ProgressBar(common.ViewletBase):
    """ Custom viewlet for workflow percentage bar
    """
    render = ViewPageTemplateFile('../zpt/progress.viewlet.pt')

    def __init__(self, context, request, view, manager=None):
        super(ProgressBar, self).__init__(context, request, view, manager)
        self._settings = None
        self._progressbar = False

    @property
    def settings(self):
        """ Settings
        """
        if self._settings is None:
            ptool = queryUtility(IProgressTool)
            self._settings = queryAdapter(ptool, ISettings)
        return self._settings

    @property
    def progressbar(self):
        """ Get progressbar for context
        """
        if self._progressbar is False:
            self._progressbar = queryMultiAdapter((self.context, self.request),
                                                  name='progress.bar')
        return self._progressbar


    @property
    def available(self):
        """ Available
        """
        if not self.progressbar:
            return False

        disabled = getattr(self.context, "disableProgressBarViewlet", None)
        if disabled:
            return False

        visibleFor = self.settings.viewletVisibleFor or []
        ctype = getattr(self.context, 'portal_type', None)
        if ctype in visibleFor:
            return True

        return False


class ProgressTrail(ProgressBar):
    """ Custom viewlet for workflow progress trail
    """
    render = ViewPageTemplateFile('../zpt/trail.viewlet.pt')

    @property
    def progressbar(self):
        """ Get progressbar for context
        """
        if self._progressbar is False:
            self._progressbar = queryMultiAdapter((self.context, self.request),
                                                  name='progress.trail')
        return self._progressbar

    @property
    def available(self):
        """ Available
        """
        if not self.progressbar:
            return False

        disabled = getattr(self.context, "disableProgressTrailViewlet", None)
        if disabled:
            return False

        visibleFor = self.settings.trailViewletVisibleFor or []
        ctype = getattr(self.context, 'portal_type', None)
        if ctype in visibleFor:
            return True

        return False

class MetadataProgress(ProgressBar):
    """ Custom viewlet for editing progress
    """
    render = ViewPageTemplateFile('../zpt/metadata.viewlet.pt')

    @property
    def progressbar(self):
        """ Get progressbar for context
        """
        if self._progressbar is False:
            self._progressbar = queryMultiAdapter((self.context, self.request),
                                                  name='progress.metadata')
        return self._progressbar

    @property
    def available(self):
        """ Available
        """
        if not self.progressbar:
            return False

        disabled = getattr(self.context,
                           "disableMetadataViewletVisibleFor", None)
        if disabled:
            return False

        visibleFor = self.settings.metadataViewletVisibleFor or []
        ctype = getattr(self.context, 'portal_type', None)
        if ctype in visibleFor:
            return True

        return False
