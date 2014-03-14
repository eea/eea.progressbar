""" View
"""
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from eea.progressbar.widgets.simple.interfaces import ISimpleWidgetEdit

class View(BrowserView):
    """ Widget view
    """
    template = ViewPageTemplateFile('view.pt')

    def __init__(self, context, request):
        super(View, self).__init__(context, request)
        self.prefix = u''
        self.title = u''
        self._ready = None

    @property
    def ready(self):
        if self._ready is None:
            field = self.context.getField(self.prefix)
            value = field.getAccessor(self.context)()
            self._ready = True if value else False
        return self._ready

    def default(self, name):
        return ISimpleWidgetEdit[name].default

    def get(self, name, default=''):
        """ Get widget value for name
        """
        value = self.default(name)
        if isinstance(value, (str, unicode)):
            value = value.format(self.title)
        return value if value else default

    def __call__(self, *args, **kwargs):
        form = self.request.form
        form.update(kwargs)

        prefix = form.get('prefix', None)
        if prefix:
            self.prefix = prefix
            self.title = prefix

        title = form.get('title', None)
        if title:
            self.title = title

        ready = form.get('ready', None)
        if ready is not None:
            self._ready = ready

        return self.template()
