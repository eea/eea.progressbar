""" Widgets interfaces
"""
from zope.interface import Interface
from zope import schema
from zope.configuration import fields
from zope.security import zcml
from zope.browserpage.metadirectives import IPageDirective
from eea.progressbar.config import EEAMessageFactory as _

class IProgressStorage(Interface):
    """ Get / update widget based progress info
    """

class IProgressWidget(Interface):
    """ Common interface to display fields within portal_progress
    """

class IProgressWidgetEdit(IProgressWidget):
    """ Common interface for widget in edit mode
    """

class IProgressWidgetView(IProgressWidget):
    """ Common interface for widget in view mode
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

    permission = zcml.Permission(
        title=_(u"Permission"),
        description=_(u"The permission needed to use the view."),
        required=False,
        )
