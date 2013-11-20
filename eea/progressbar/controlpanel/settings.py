""" Control Panel
"""
from zope.component import queryUtility
from zope.interface import implements
from eea.progressbar.controlpanel.interfaces import ISettings
from eea.progressbar.controlpanel.interfaces import _
from plone.app.controlpanel.form import ControlPanelForm
from plone.registry.interfaces import IRegistry
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from zope.formlib import form

class ControlPanel(ControlPanelForm):
    """ Diffbot API
    """
    form_fields = form.FormFields(ISettings)
    label = _(u"Progress Bar Settings")
    description = _(u"Progress bar settings")
    form_name = _(u"Progress bar settings")

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
