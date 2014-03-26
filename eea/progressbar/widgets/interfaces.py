""" Widgets interfaces
"""
from zope.interface import Interface
from zope import schema
from zope.configuration import fields
from zope.security import zcml
from zope.browserpage.metadirectives import IPageDirective
from eea.progressbar.config import EEAMessageFactory as _

class IProgressWidget(Interface):
    """ Common interface to display fields within portal_progress
    """

class IProgressWidgetEdit(IProgressWidget):
    """ Common interface for widget in edit mode
    """

class IProgressWidgetView(IProgressWidget):
    """ Common interface for widget in view mode
    """
    prefix = schema.TextLine(
        title=_(u'Prefix'),
        description=_(u"Usually a schema field name")
    )

    custom = schema.Bool(
        title=_(u"Custom"),
        description=_(u"Is this widget customized?"),
        readonly=True
    )

    hidden = schema.Bool(
        title=_(u"Hidden"),
        description=_(u"Is this widget hidden?"),
        readonly=True
    )

    def setPrefix(prefix):
        """ Update prefix
        """

    def default(name):
        """ Get default value of a property given by name
        """

    def ready(context):
        """ For the given context was this property correctly set
        """

    def get(name, default):
        """ Get widget configuration by given name or return the default value
        """

    def translate(message):
        """ Use zope.i18n to translate message
        """

    def __call__(args, kwargs):
        """ Render widget
        """


class IProgressWidgets(Interface):
    """ Utility to get available progressbar widgets
    """

class IWidgetDirective(IPageDirective):
    """ Progress bar widget directive
    """
    for_ = fields.GlobalObject(
        title=u"The interface or class this view is for.",
        required=False
        )

    view = fields.GlobalObject(
        title=_(u"View"),
        description=_(u"A class that provides attributes used by the view."),
        required=True,
        )

    edit = fields.GlobalObject(
        title=_(u"Edit"),
        description=_(u"A class that provides attributes used by the edit."),
        required=True,
        )

    name = schema.TextLine(
        title=u"The name of the field from ctype Schema",
        description=_(u""
            u"E.g. prgressbar.widget.title or progressbar.widget.relatedItems"),
        required=False
        )

    layer = fields.GlobalInterface(
        title=_(u"The layer the view is in."),
        description=_(u"""
        A skin is composed of layers. It is common to put skin
        specific views in a layer named after the skin. If the 'layer'
        attribute is not supplied, it defaults to 'default'."""),
        required=False,
        )

    edit_permission = zcml.Permission(
        title=_(u"Edit Permission"),
        description=_(u"The permission needed to edit this widget."),
        required=False,
        )

    view_permission = zcml.Permission(
        title=_(u"View Permission"),
        description=_(u"The permission needed to view this widget."),
        required=False,
        )

    permission = zcml.Permission(
        title=_(u"Permission"),
        description=_(u"The permission needed to use the view or edit"),
        required=False
        )
