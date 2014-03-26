""" Control Panel
"""
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
from zope.component import queryUtility, getMultiAdapter
from zope.interface import implements
from zope.formlib import form
from zope.schema.interfaces import IVocabularyFactory
from plone.app.controlpanel.form import ControlPanelForm
from plone.app.form.validators import null_validator
from plone.registry.interfaces import IRegistry
from plone.protect import CheckAuthenticator
from plone.app.controlpanel.events import ConfigurationChangedEvent
from plone.app.controlpanel.widgets import MultiCheckBoxVocabularyWidget
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from eea.progressbar.controlpanel.interfaces import ISettings
from eea.progressbar.controlpanel.interfaces import _

class ControlPanel(ControlPanelForm):
    """ Diffbot API
    """
    form_fields = form.FormFields(ISettings)
    form_fields[
      'viewletVisibleFor'].custom_widget = MultiCheckBoxVocabularyWidget
    form_fields[
      'trailViewletVisibleFor'].custom_widget = MultiCheckBoxVocabularyWidget
    form_fields[
      'metadataViewletVisibleFor'].custom_widget = MultiCheckBoxVocabularyWidget

    label = _(u"Progress Bar Settings")
    description = _(u"Progress bar settings")
    form_name = _(u"Progress bar settings")

    @form.action(_(u'label_save', default=u'Save'), name=u'save')
    def handle_edit_action(self, action, data):
        """ Save
        """
        CheckAuthenticator(self.request)
        if form.applyChanges(self.context, self.form_fields, data,
                             self.adapters):
            self.status = _("Changes saved.")
            notify(ConfigurationChangedEvent(self, data))
            self._on_save(data)
        else:
            self.status = _("No changes made.")

    @form.action(_(u'label_back', default=u'Back'),
                 validator=null_validator,
                 name=u'cancel')
    def handle_cancel_action(self, action, data):
        """ Cancel
        """
        url = getMultiAdapter((self.context, self.request),
                              name='absolute_url')()
        self.request.response.redirect(url)
        return ''

class ControlPanelAdapter(SchemaAdapterBase):
    """ Form adapter
    """
    implements(ISettings)

    def __init__(self, context):
        super(ControlPanelAdapter, self).__init__(context)
        self._settings = None

    @property
    def settings(self):
        """ Settings
        """
        if self._settings is None:
            self._settings = queryUtility(
                IRegistry).forInterface(ISettings, False)
        return self._settings

    @property
    def viewletVisibleFor(self):
        """ Getter
        """
        name = u"viewletVisibleFor"
        return getattr(self.settings, name, ISettings[name].default)

    @viewletVisibleFor.setter
    def viewletVisibleFor(self, value):
        """ Setter
        """
        self.settings.viewletVisibleFor = value

    @property
    def trailViewletVisibleFor(self):
        """ Getter
        """
        name = u"trailViewletVisibleFor"
        return getattr(self.settings, name, ISettings[name].default)

    @trailViewletVisibleFor.setter
    def trailViewletVisibleFor(self, value):
        """ Setter
        """
        self.settings.trailViewletVisibleFor = value

    @property
    def hidedStatesPercentage(self):
        """ Getter
        """
        name = u"hidedStatesPercentage"
        return getattr(self.settings, name, ISettings[name].default)

    @hidedStatesPercentage.setter
    def hidedStatesPercentage(self, value):
        """ Setter
        """
        try:
            value = int(value)
        except Exception:
            value = 0
        self.settings.hidedStatesPercentage = value

    @property
    def metadataViewletVisibleFor(self):
        """ Getter
        """
        name = u"metadataViewletVisibleFor"
        return getattr(self.settings, name, ISettings[name].default)

    @metadataViewletVisibleFor.setter
    def metadataViewletVisibleFor(self, value):
        """ Setter
        """
        self.settings.metadataViewletVisibleFor = value
        voc = queryUtility(IVocabularyFactory,
                        name=u'eea.progressbar.vocabulary.MetadataContentTypes')
        existing = [item for item in voc.existing]
        for item in value:
            if item in existing:
                continue

            oid = item.lower().replace(' ', '-')
            oid = self.context.invokeFactory('ProgressContentType',
                                             id=oid, title=item)
            child = self.context[oid]
            child.getField('ctype').getMutator(child)(item)
            notify(ObjectModifiedEvent(child))
