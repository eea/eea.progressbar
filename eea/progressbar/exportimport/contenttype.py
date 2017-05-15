""" XML Adapter
"""
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
from zope.component import queryMultiAdapter
from Products.GenericSetup.interfaces import IBody
from Products.GenericSetup.utils import XMLAdapterBase
from eea.progressbar.interfaces import IContentType
from eea.progressbar.content.contenttype import EditSchema

class ContentTypeXMLAdapter(XMLAdapterBase):
    """ Generic setup import/export xml adapter
    """
    __used_for__ = IContentType

    def _exportNode(self):
        """Export the object as a DOM node.
        """
        node = self._getObjectNode('object')
        fields = ['title']
        fields.extend(field.getName() for field in EditSchema.fields())
        for prop in fields:
            child = self._doc.createElement('property')
            child.setAttribute('name', prop)
            field = self.context.getField(prop)
            value = field.getAccessor(self.context)()
            value = self._doc.createTextNode(str(value))
            child.appendChild(value)
            node.appendChild(child)

        for child in self.context.objectValues():
            element = self._doc.createElement('object')
            element.setAttribute('name', child.getId())
            element.setAttribute('meta_type', child.meta_type)
            node.appendChild(element)

        # Editing progress
        exporter = queryMultiAdapter((self.context, self.environ), IBody,
                                     name='metadata.progress.xml')
        node.appendChild(exporter.node)
        return node

    def _importNode(self, node):
        """Import the object from the DOM node.
        """
        for child in node.childNodes:
            # Properties
            if child.nodeName == 'property':
                name = child.getAttribute('name')
                value = self._getNodeText(child)
                value = value.decode('utf-8')
                purge = child.getAttribute('purge')
                purge = self._convertToBoolean(purge)
                if purge:
                    value = u''
                field = self.context.getField(name)
                field.getMutator(self.context)(value)
                notify(ObjectModifiedEvent(self.context))

            # Editing progress
            elif child.nodeName == 'progress':
                importer = queryMultiAdapter((self.context, self.environ),
                                            IBody, name='metadata.progress.xml')
                importer.node = child

        self.context.reindexObject()

    node = property(_exportNode, _importNode)
