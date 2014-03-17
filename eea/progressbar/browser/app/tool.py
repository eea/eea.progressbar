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
            # Skip some fields
            if field.getName() == 'id':
                continue

            # Skip invisible fields
            visible = getattr(field.widget, 'visible', None)
            if isinstance(visible, (bool, int)):
                if not visible:
                    continue
            elif isinstance(visible, dict):
                if visible.get('edit', u'visible') != u'visible':
                    continue

            yield field

    def view(self, field):
        """ Widget view
        """
        ctype = getattr(self.context, '.schema', None)
        widget = queryMultiAdapter((ctype, self.request),
                                    name=u'progressbar.widget.view')
        widget.setPrefix(field.getName())
        widget.label = field.widget.label
        widget.field = field
        return widget

    def edit(self, field):
        """ Widget edit
        """
        ctype = getattr(self.context, '.schema', None)
        widget = queryMultiAdapter((ctype, self.request),
                                    name=u'progressbar.widget.edit')
        widget.setPrefix(field.getName())
        widget.field = field
        return widget
