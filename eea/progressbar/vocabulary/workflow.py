""" Content types
"""
import operator
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from Products.CMFCore.utils import getToolByName

class States(object):
    """ Metadata content types
    """
    implements(IVocabularyFactory)

    def __call__(self, context=None):
        """ See IVocabularyFactory interface
        """
        wftool = getToolByName(context, 'portal_workflow')
        workflows = wftool.getWorkflowsFor(context)

        items = set([SimpleTerm(u'all', u'all', u'All')])
        for wf in workflows:
            for key, state in wf.states.items():
                item = SimpleTerm(key, key, state.title or key)
                items.add(item)

        return SimpleVocabulary(sorted(items, key=operator.attrgetter('title')))
