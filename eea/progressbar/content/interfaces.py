"""
Progress content interfaces

    >>> portal = layer['portal']

"""
from zope.interface import Interface

class IProgressTool(Interface):
    """
    Local utility to store and customize content-types schema progress

        >>> from zope.component import queryUtility
        >>> from eea.progressbar.interfaces import IProgressTool
        >>> ptool = queryUtility(IProgressTool)
        >>> ptool
        <ProgressTool at /plone/portal_progress>

    """

class IContentType(Interface):
    """
    Content-type

        >>> cid = ptool.invokeFactory('ProgressContentType', id='Document')
        >>> ctype = ptool[cid]
        >>> ctype
        <ProgressContentType at /plone/portal_progress/Document>

        >>> ctype.getField('ctype').getAccessor(ctype)()
        ''

        >>> form = {'ctype': 'Document'}
        >>> ctype.processForm(values=form, data=1,
        ...                   metadata=1, REQUEST=portal.REQUEST)
        >>> ctype.getField('ctype').getAccessor(ctype)()
        'Document'

    """
