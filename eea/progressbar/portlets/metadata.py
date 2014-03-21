""" Progress bar portlets
"""
from zope import schema
from zope.formlib import form
from zope.interface import implements
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from eea.progressbar.config import EEAMessageFactory as _

class IMetadataPortlet(IPortletDataProvider):
    """ Progress bar portlet
    """
    label = schema.TextLine(
        title=_(u"Porlet title"),
        description=_(u"Title of the portlet. Leave empty if you don't want "
                      u"to display a title for this portlet"),
        default=u"Editing progress",
        required=False
    )

class Assignment(base.Assignment):
    """ Assignment
    """
    implements(IMetadataPortlet)

    def __init__(self, label=u"Editing progress"):
        self.label = label

    @property
    def title(self):
        """ Get portlet title
        """
        return self.label or u"Editing progress"

class AddForm(base.AddForm):
    """ Add portlet
    """
    form_fields = form.Fields(IMetadataPortlet)
    label = _(u"Add Editing progress portlet")
    description = _(u"This portlet shows editing progress information")

    def create(self, data):
        """ Create
        """
        return Assignment(label=data.get('label', u"Editing progress"))

class EditForm(base.EditForm):
    """ Portlet edit
    """
    form_fields = form.Fields(IMetadataPortlet)
    label = _(u"Edit Editing progress portlet")
    description = _(u"This portlet shows editing progress information")

class Renderer(base.Renderer):
    """ portlet renderer
    """
    render = ViewPageTemplateFile('metadata.pt')

    @property
    def available(self):
        """By default, portlets are available
        """
        return getToolByName(
            self.context, 'portal_membership').checkPermission(
                'Review portal content', self.context)
