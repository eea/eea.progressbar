""" XML Adapter
"""
import logging
from zope import schema
from zope.component import queryMultiAdapter, queryAdapter
from Products.GenericSetup.utils import XMLAdapterBase
from Products.GenericSetup.interfaces import IBody
from eea.progressbar.interfaces import IProgressTool
from eea.progressbar.interfaces import ISettings
logger = logging.getLogger('eea.progressbar')

class ProgressToolXMLAdapter(XMLAdapterBase):
    """ Generic setup export/import xml adapter
    """
    __used_for__ = IProgressTool

    def _exportBody(self):
        """Export the object as a file body.
        """
        self._doc.appendChild(self._exportNode())
        xml = self._doc.toprettyxml(' ', encoding='utf-8')
        self._doc.unlink()
        return xml
    body = property(_exportBody, XMLAdapterBase._importBody)

    def _exportNode(self):
        """Export the object as a DOM node.
        """
        node = self._getObjectNode('object')
        settings = queryAdapter(self.context, ISettings)
        for name, _field in schema.getFieldsInOrder(ISettings):
            child = self._doc.createElement('property')
            child.setAttribute('name', name)
            value = getattr(settings, name)
            if isinstance(value, (tuple, list)):
                for item in value:
                    if not value:
                        continue
                    element = self._doc.createElement('element')
                    element.setAttribute('value', item)
                    child.appendChild(element)
            else:
                if isinstance(value, (bool, int)):
                    value = repr(value)
                value = self._doc.createTextNode(value)
                child.appendChild(value)
            node.appendChild(child)

        for child in self.context.objectValues():
            exporter = queryMultiAdapter((child, self.environ), IBody)
            node.appendChild(exporter.node)
        return node

    def _importNode(self, node):
        """Import the object from the DOM node.
        """
        purge = node.getAttribute('purge')
        purge = self._convertToBoolean(purge)
        if purge:
            self.context.manage_delObjects(self.context.objectIds())

        settings = queryAdapter(self.context, ISettings)
        for child in node.childNodes:
            # Handle properties
            if child.nodeName == 'property':
                name = child.getAttribute('name')
                purge = child.getAttribute('purge')
                purge = self._convertToBoolean(purge)
                elements = []
                for element in child.childNodes:
                    if element.nodeName != 'element':
                        continue
                    elements.append(element.getAttribute('value'))
                if elements:
                    value = (not purge) and elements or []
                else:
                    value = self._getNodeText(child)
                    value = value.decode('utf-8')
                    value = (not purge) and value or u''
                try:
                    setattr(settings, name, value)
                except Exception, err:
                    logger.exception(err)
                    continue

            # Handle objects
            elif child.nodeName == 'object':
                purge_child = child.getAttribute('purge')
                purge_child = self._convertToBoolean(purge_child)
                name = child.getAttribute('name').encode('utf-8')
                obj_ids = self.context.objectIds()
                if purge_child:
                    if name in obj_ids:
                        self.context.manage_delObjects([name, ])
                    continue

                obj = self.context._getOb(name, None)
                if not obj:
                    portal_type = child.getAttribute(
                        'meta_type').encode('utf-8')
                    name = self.context.invokeFactory(portal_type, name)
                    obj = self.context._getOb(name)

                importer = queryMultiAdapter((obj, self.environ), IBody)
                importer.node = child

    node = property(_exportNode, _importNode)
