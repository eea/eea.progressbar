""" View
"""
from zope.component import queryUtility, queryAdapter
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.pagetemplate.engine import TrustedEngine, TrustedZopeContext
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from eea.progressbar.widgets.simple.interfaces import ISimpleWidgetEdit
from eea.progressbar.widgets.view import ViewForm
from eea.progressbar.interfaces import IStorage

class View(ViewForm):
    """ Widget view
    """
    template = ViewPageTemplateFile('view.pt')

    def default(self, name):
        """ Default values
        """
        return ISimpleWidgetEdit[name].default

    @property
    def custom(self):
        """ Is customized
        """
        if self._custom is None:
            storage = queryAdapter(self.parent, IStorage)
            field = storage.field(self.prefix, {})
            value = field.get('states', None)
            if value is not None:
                self._custom = True
            else:
                self._custom = False
        return self._custom

    def condition(self, context=None):
        """ Get condition
        """
        if not context:
            context = self.context
        field = context.getField(self.prefix)
        value = field.getAccessor(context)()
        condition = self.get('condition')
        engine = TrustedEngine
        zopeContext = TrustedZopeContext(engine, {
            'context': context,
            'request': self.request,
            'field': field,
            'value': value
        })
        expression = engine.compile(condition)
        result = zopeContext.evaluate(expression)
        if callable(result):
            result = result()
        return result

    def ready(self, context=None):
        """ Is ready
        """
        if self._ready is None:
            self._ready = self.condition(context)
        return self._ready

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
