""" Edit widget
"""
from zope.formlib.form import Fields
from plone.app.controlpanel.widgets import MultiCheckBoxVocabularyWidget
from eea.progressbar.widgets.simple.interfaces import ISimpleWidgetEdit
from eea.progressbar.widgets.edit import EditForm

class Edit(EditForm):
    """ Simple widget edit form
    """
    form_fields = Fields(ISimpleWidgetEdit)
    form_fields['states'].custom_widget = MultiCheckBoxVocabularyWidget
