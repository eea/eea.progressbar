""" Tool views
"""
from Products.Five.browser import BrowserView

class ContentType(BrowserView):
    """ Configure content-type
    """
    def schema(self):
        """ Schema
        """
        schema = getattr(self.context, '.schema', None)
        schema = getattr(schema, 'Schema', lambda: None)
        schema = schema()

        if not schema:
            return

        for field in schema.fields():
            yield field
