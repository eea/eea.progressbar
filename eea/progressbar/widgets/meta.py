""" Custom meta-directives DaViz Views
"""
from zope.interface import implements, Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from Products.Five.browser.metaconfigure import page
from eea.progressbar.widgets.interfaces import IProgressWidgets

class ProgressbarWidgets(object):
    """ Registry for progressbar widgets registered via ZCML
    """
    implements(IProgressWidgets)
    _views = {}
    _edits = {}

    @property
    def views(self):
        """ Views
        """
        return self._views

    @property
    def edits(self):
        """ Edits
        """
        return self._edits

    def keys(self):
        """ Views names
        """
        return self.views.keys()

    def edit_keys(self):
        """ Edits names
        """
        return self.edits.keys()

    def __call__(self, mode='view'):
        if mode != 'view':
            return self.edit_keys()
        return self.keys()

def WidgetDirective(_context, name=u"progressbar.widget",
                    view=None,
                    edit=None,
                    permission=None,
                    edit_permission=None,
                    view_permission=None,
                    for_=Interface,
                    layer=IDefaultBrowserLayer):
    """ Progress bar widget
    """

    view_name = name + '.view'
    if not view_permission:
        view_permission = permission
    page(_context=_context, name=view_name, permission=view_permission,
         for_=for_, layer=layer, class_=view)

    ProgressbarWidgets._views[name] = name

    edit_name = name + '.edit'
    if not edit_permission:
        edit_permission = permission
    page(_context=_context, name=edit_name, permission=edit_permission,
         for_=for_, layer=layer, class_=edit)

    ProgressbarWidgets._edits[name] = name
