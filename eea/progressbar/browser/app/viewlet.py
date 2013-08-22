""" Custom viewlets
"""
from plone.app.layout.viewlets import common
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class ProgressBar(common.ViewletBase):
    """ Custom viewlet for progressbar
    """
    render = ViewPageTemplateFile('../zpt/viewlet.pt')

    @property
    def available(self):
        """ Available
        """
        return True
