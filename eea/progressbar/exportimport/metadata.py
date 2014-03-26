""" XML Adapter
"""
from zope.component import queryAdapter
from Products.GenericSetup.utils import XMLAdapterBase
from eea.progressbar.interfaces import IContentType
from eea.progressbar.interfaces import IStorage

class MetadataXMLAdapter(XMLAdapterBase):
    """ Generic setup export/import xml adapter
    """
    __used_for__ = IContentType

    def _exportNode(self):
        """Export the object as a DOM node.
        """
        node = self._doc.createElement('progress')
        storage = queryAdapter(self.context, IStorage)

        # Fields order
        order = storage.order
        if order:
            child = self._doc.createElement('property')
            child.setAttribute('name', 'order')
            for name in order:
                element = self._doc.createElement('element')
                element.setAttribute('value', name)
                child.appendChild(element)
            node.appendChild(child)

        # Fields
        fields = storage.fields
        if fields:
            for name, field in fields.items():
                child = self._doc.createElement('field')
                child.setAttribute('name', name)

                for key, value in field.items():
                    if key == 'name':
                        continue
                    prop = self._doc.createElement('property')
                    prop.setAttribute('name', key)
                    if isinstance(value, (tuple, list)):
                        for item in value:
                            if not item:
                                continue
                            element = self._doc.createElement('element')
                            element.setAttribute('value', item)
                            prop.appendChild(element)
                    else:
                        if isinstance(value, (bool, int, float, basestring)):
                            value = str(value)
                        text = self._doc.createTextNode(value)
                        prop.appendChild(text)
                    child.appendChild(prop)
                node.appendChild(child)
        return node

    def _importNode(self, node):
        """Import the object from the DOM node.
        """
        storage = queryAdapter(self.context, IStorage)

        for child in node.childNodes:
            # Order
            if child.nodeName == 'property':
                name = child.getAttribute('name')
                if name == 'order':
                    elements = []
                    for element in child.childNodes:
                        if element.nodeName != 'element':
                            continue
                        elements.append(
                            element.getAttribute('value').encode('utf-8')
                        )
                    if elements:
                        storage.reorder(elements)

            elif child.nodeName == 'field':
                name = child.getAttribute('name')

                field = {}
                for prop in child.childNodes:
                    if prop.nodeName != 'property':
                        continue

                    key = prop.getAttribute('name')
                    elements = []
                    for element in prop.childNodes:
                        if element.nodeName != 'element':
                            continue
                        elements.append(
                            element.getAttribute('value').encode('utf-8')
                        )
                    if elements:
                        field[key] = elements
                    else:
                        value = self._getNodeText(prop).encode('utf-8')
                        if value.lower() in ('true', 'on', 'yes'):
                            value = True
                        elif value.lower() in ('false', 'off', 'no'):
                            value = False
                        field[key] = value
                storage.edit_field(name, **field)

    node = property(_exportNode, _importNode)
