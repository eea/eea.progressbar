""" Abstract Edit widget
"""
from zope.component import queryAdapter
from zope.formlib.form import SubPageForm
from zope.formlib.form import action as formAction
from zope.formlib.form import setUpWidgets, haveInputWidgets
from Products.statusmessages.interfaces import IStatusMessage
from eea.progressbar.interfaces import IStorage
from eea.progressbar.config import  EEAMessageFactory as _

class EditForm(SubPageForm):
    """
    Basic layer to edit progress widgets

    Assign these attributes in your subclass:
      - form_fields: Fields(Interface)

    """
    form_fields = None

    def __init__(self, context, request):
        super(EditForm, self).__init__(context, request)
        self.parent = self.context.getParentNode()
        for key in self.request.form:
            if key.endswith('.labelEmpty'):
                self.prefix = key.split('.')[0]
                break

    @property
    def _data(self):
        """ Return view
        """
        storage = queryAdapter(self.parent, IStorage)
        return storage.field(self.prefix, {})

    def setUpWidgets(self, ignore_request=False):
        """ Sets up widgets
        """
        self.adapters = {}

        for key, value in self.request.form.items():
            if isinstance(value, str):
                value = value.decode('utf-8')
                self.request.form[key] = value

        self.widgets = setUpWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            form=self, data=self._data, adapters=self.adapters,
            ignore_request=ignore_request)

    @formAction(_('Save'), condition=haveInputWidgets)
    def save(self, action, data):
        """ Handle save action
        """
        storage = queryAdapter(self.parent, IStorage)
        storage.edit_field(self.prefix, **data)

        name = action.__name__.encode('utf-8')
        value = self.request.form.get(name, '')
        if value == 'ajax':
            return _(u"Changes saved")
        return self.nextUrl

    @formAction(_('Reset'), condition=haveInputWidgets)
    def reset(self, action, data):
        """ Handle save action
        """
        storage = queryAdapter(self.parent, IStorage)
        storage.delete_field(self.prefix)

        name = action.__name__.encode('utf-8')
        value = self.request.form.get(name, '')
        if value == 'ajax':
            return _(u"Changes saved")
        return self.nextUrl

    @property
    def nextUrl(self):
        """ Redirect to view as next_url
        """
        status = queryAdapter(self.request, IStatusMessage)
        status.addStatusMessage(_('Changes saved'), type='info')
        next_url = self.parent.absolute_url()
        self.request.response.redirect(next_url)
