""" Abstract Edit widget
"""
from zope.formlib.form import SubPageForm
from zope.formlib.form import action, setUpWidgets
from eea.progressbar.config import  EEAMessageFactory as _

class EditForm(SubPageForm):
    """
    Basic layer to edit progress widgets

    Assign these attributes in your subclass:
      - form_fields: Fields(Interface)

    """
    form_fields = None

    @property
    def _data(self):
        """ Return view
        """
        return {}

    def setUpWidgets(self, ignore_request=False):
        """ Sets up widgets
        """
        self.adapters = {}
        self.widgets = setUpWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            form=self, data=self._data, adapters=self.adapters,
            ignore_request=ignore_request)

    @action(_('Save'))
    def save(self, saction, data):
        """ Handle save action
        """
        raise NotImplementedError
