""" Workflow progress monitoring adapters for GenericSetup
"""
from zope.component import queryMultiAdapter
from Products.GenericSetup.utils import XMLAdapterBase
from Products.GenericSetup.interfaces import IBody
from Products.CMFPlone.utils import base_hasattr
from eea.progressbar.interfaces import IWorkflowTool
from eea.progress.workflow.interfaces import IWorkflow, IWorkflowState
from eea.progressbar.config import PROGRESSFILE

class WorkflowToolXMLAdapter(XMLAdapterBase):
    """ Generic setup import/export xml adapter
    """
    __used_for__ = IWorkflowTool

    def _exportNode(self):
        """Export the object as a DOM node.
        """
        node = self._getObjectNode('object')
        for child in self.context.objectValues():
            exporter = queryMultiAdapter((child, self.environ), IBody,
                                         name=PROGRESSFILE)
            node.appendChild(exporter.node)
        return node

    def _importNode(self, node):
        """Import the object from the DOM node.
        """
        for child in node.childNodes:
            if child.nodeName != 'object':
                continue

            name = child.getAttribute('name').encode('utf-8')
            obj = self.context._getOb(name, None)
            importer = queryMultiAdapter((obj, self.environ), IBody,
                                         name=PROGRESSFILE)
            if not importer:
                continue
            importer.node = child

    node = property(_exportNode, _importNode)

class WorkflowXMLAdapter(XMLAdapterBase):
    """ Generic setup import/export xml adapter
    """
    __used_for__ = IWorkflow

    def _exportNode(self):
        """Export the object as a DOM node.
        """
        node = self._getObjectNode('object')
        for child in self.context.states.values():
            exporter = queryMultiAdapter((child, self.environ), IBody,
                                         name=PROGRESSFILE)
            node.appendChild(exporter.node)
        return node

    def _importNode(self, node):
        """Import the object from the DOM node.
        """
        for child in node.childNodes:
            if child.nodeName != 'object':
                continue

            name = child.getAttribute('name').encode('utf-8')
            obj = self.context.states.get(name, None)
            importer = queryMultiAdapter((obj, self.environ), IBody,
                                         name=PROGRESSFILE)
            if not importer:
                continue
            importer.node = child

    node = property(_exportNode, _importNode)

class WorkflowStateXMLAdapter(XMLAdapterBase):
    """ Generic setup import/export xml adapter
    """
    __used_for__ = IWorkflowState

    def _exportNode(self):
        """Export the object as a DOM node.
        """
        node = self._getObjectNode('object')
        progress = (self.context.progress if
                    base_hasattr(self.context, 'progress') else None)
        if progress is None:
            return node

        child = self._doc.createElement('property')
        child.setAttribute('name', 'progress')
        value = self._doc.createTextNode(repr(progress))
        child.appendChild(value)
        node.appendChild(child)
        return node

    def _importNode(self, node):
        """Import the object from the DOM node.
        """
        for child in node.childNodes:
            if child.nodeName != 'property':
                continue

            name = child.getAttribute('name')
            remove = child.getAttribute('remove')
            remove = self._convertToBoolean(remove)

            if hasattr(self.context, name) and remove:
                delattr(self.context, name)
                continue

            value = int(self._getNodeText(child))
            override = child.getAttribute('override')
            override = self._convertToBoolean(override)

            if hasattr(self.context, name) and (not override):
                continue

            setattr(self.context, name, value)

    node = property(_exportNode, _importNode)
