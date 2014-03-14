""" Tool views
"""
from zope.component import queryMultiAdapter
from Products.Five.browser import BrowserView

class ContentType(BrowserView):
    """ Configure content-type
    """
    def schema(self):
        """ Schema
        """
        ctype = getattr(self.context, '.schema', None)
        schema = getattr(ctype, 'Schema', lambda: None)
        schema = schema()

        if not schema:
            return

        for field in schema.fields():
            yield field

    def view(self, field):
        """ Widget view
        """
        ctype = getattr(self.context, '.schema', None)
        widget = queryMultiAdapter((ctype, self.request),
                                    name=u'progressbar.widget.view')
        widget.prefix = field.getName()
        widget.title = field.widget.label
        return widget()

    def edit(self, field):
        """ Widget edit
        """
        ctype = getattr(self.context, '.schema', None)
        widget = queryMultiAdapter((ctype, self.request),
                                    name=u'progressbar.widget.edit')
        widget.prefix = field.getName()
        return widget()
