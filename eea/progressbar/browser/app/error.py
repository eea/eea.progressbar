""" Errors
"""
import logging
from pprint import pformat
from zope.component import queryAdapter
from Products.Five.browser import BrowserView
from eea.progressbar.interfaces import IStorage

logger = logging.getLogger('eea.progressbar')

class Error(BrowserView):
    """ Render an error message when something is wrong with widgets
    """
    def __call__(self, **kwargs):
        error = kwargs.get('error', None)
        fid = kwargs.get('fid', '')
        msg = ''
        if fid:
            storage = queryAdapter(self.context.getParentNode(), IStorage)
            if storage:
                data = storage.field(fid)
                if data:
                    msg = pformat(data.__dict__)

        logger.exception('\n%s\n', msg)
        return self.index(error=error)
