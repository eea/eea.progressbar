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

class ITrailPortlet(IPortletDataProvider):
    """ Progress bar portlet
    """
    label = schema.TextLine(
        title=_(u"Porlet title"),
        description=_(u"Title of the portlet. Leave empty if you don't want "
                      "to display a title for this portlet"),
        default=u"Status",
        required=False
    )

class Assignment(base.Assignment):
    """ Assignment
    """
    implements(ITrailPortlet)

    def __init__(self, label=u"Status"):
        self.label = label

    @property
    def title(self):
        """ Get portlet title
        """
        return self.label or u'Workflow State Trail'

class AddForm(base.AddForm):
    """ Add portlet
    """
    form_fields = form.Fields(ITrailPortlet)
    label = _(u"Add Workflow states trail portlet")
    description = _(u"This portlet shows workflow states trail information")

    def create(self, data):
        """ Create
        """
        return Assignment(label=data.get('label', u'Status'))

class EditForm(base.EditForm):
    """ Portlet edit
    """
    form_fields = form.Fields(ITrailPortlet)
    label = _(u"Edit Workflow State Trail portlet")
    description = _(u"This portlet shows workflow states trail information")

class Renderer(base.Renderer):
    """ portlet renderer
    """
    render = ViewPageTemplateFile('trail.pt')

    @property
    def available(self):
        """By default, portlets are available
        """
        return getToolByName(
            self.context, 'portal_membership').checkPermission(
                'Review portal content', self.context)
