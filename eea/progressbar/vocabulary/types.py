""" Content types
"""
from zope.component import queryUtility, queryAdapter
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm

from eea.progressbar.interfaces import IProgressTool
from eea.progressbar.interfaces import ISettings


class Metadata(object):
    """ Metadata content types
    """
    implements(IVocabularyFactory)

    @property
    def existing(self):
        """ Existing ctypes
        """
        ptool = queryUtility(IProgressTool)
        for child in ptool.objectValues():
            yield child.getField('ctype').getAccessor(child)()

    @property
    def allowed(self):
        """ Allowed ctypes
        """
        tool = queryUtility(IProgressTool)
        settings = queryAdapter(tool, ISettings)
        return settings.metadataViewletVisibleFor or []

    def __call__(self, context=None):
        """ See IVocabularyFactory interface
        """
        existing = [item for item in self.existing]
        allowed = self.allowed

        items = [SimpleTerm(item, item, item)
                 for item in allowed if item not in existing]
        return SimpleVocabulary(items)
