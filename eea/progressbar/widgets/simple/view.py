""" View
"""
from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from eea.progressbar.widgets.simple.interfaces import ISimpleWidgetEdit
from eea.progressbar.widgets.view import ViewForm

class View(ViewForm):
    """ Widget view
    """
    template = ViewPageTemplateFile('view.pt')

    def default(self, name):
        """ Default values
        """
        return ISimpleWidgetEdit[name].default

    def workflow(self):
        """ Human readable workflow states
        """
        value = self.get('states', [])
        items = (SimpleTerm(key, key, key) for key in value)
        vocabulary = ISimpleWidgetEdit['states'].value_type.vocabularyName
        if not vocabulary:
            return items

        voc = queryUtility(IVocabularyFactory, name=vocabulary)
        if not voc:
            return items

        return [term for term in voc(self.context) if term.value in value]
