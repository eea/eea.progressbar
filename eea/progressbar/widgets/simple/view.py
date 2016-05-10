""" View
"""
from Acquisition import ImplicitAcquisitionWrapper
from logging import getLogger

from zope.interface import implements

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from eea.progressbar.interfaces import IStorage
from eea.progressbar.widgets.simple.interfaces import ISimpleWidgetEdit
from eea.progressbar.widgets.simple.interfaces import ISimpleWidgetView
from eea.progressbar.widgets.view import ViewForm
from zope.component import queryUtility, queryAdapter
from zope.pagetemplate.engine import TrustedEngine, TrustedZopeContext
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm

logger = getLogger('eea.progressbar')


class View(ViewForm):
    """ Widget view
    """
    implements(ISimpleWidgetView)
    template = ViewPageTemplateFile('view.pt')

    def __init__(self, context, request):
        super(View, self).__init__(context, request)
        self._workflow = None
        self._condition = None

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
            self._custom = True if value is not None else False
        return self._custom

    @property
    def hidden(self):
        """ Is this hidden?
        """
        if self._hidden is None:
            self._hidden = False if self.workflow() else True
        return self._hidden

    def ready(self, context=None):
        """ Is ready
        """
        if self._ready is None:
            self._ready = self.condition(context)
        return self._ready

    def workflow(self):
        """ Human readable workflow states
        """
        if self._workflow is None:
            value = self.get('states', [])
            self._workflow = (SimpleTerm(key, key, key) for key in value)
            if self._workflow:
                self._hidden = False
            else:
                self._hidden = True

            vocabulary = ISimpleWidgetEdit['states'].value_type.vocabularyName
            if not vocabulary:
                return self._workflow

            voc = queryUtility(IVocabularyFactory, name=vocabulary)
            if not voc:
                return self._workflow

            self._workflow = [term for term in voc(self.context)
                              if term.value in value]
        return self._workflow

    def condition(self, context=None):
        """ Get condition
        """
        if self._condition is None:
            if not context:
                context = self.context
            field = (context.getField(self.prefix)
                     if getattr(context, 'getField', None) else None)
            value = (field.getAccessor(context)() if field
                     else getattr(context, self.prefix, None))
            condition = self.get('condition')
            engine = TrustedEngine
            zopeContext = TrustedZopeContext(engine, {
                'context': context,
                'request': self.request,
                'field': field,
                'value': value
            })
            expression = engine.compile(condition)

            try:
                result = zopeContext.evaluate(expression)
            except Exception, err:
                logger.exception(err)
                result = False

            if callable(result) and \
                not isinstance(result, ImplicitAcquisitionWrapper):
                result = result()

            self._condition = result
        return self._condition
