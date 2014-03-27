""" Tool views
"""
from zope.component import queryMultiAdapter, queryAdapter
from Products.Five.browser import BrowserView
from Products.GenericSetup.interfaces import IBody
from Products.statusmessages.interfaces import IStatusMessage
from Products.GenericSetup.context import SnapshotExportContext
from Products.GenericSetup.context import SnapshotImportContext
from eea.progressbar.interfaces import IStorage
from eea.progressbar.config import EEAMessageFactory as _

class ContentType(BrowserView):
    """ Configure content-type
    """
    def __init__(self, context, request):
        super(ContentType, self).__init__(context, request)
        self._field = None

    def reorder(self, fields, order):
        """ Reorder fields by given order
        """
        yielded = set()

        # Yield fields that are in order
        for name in order:
            for field in fields:
                if field.getName() == name:
                    yielded.add(name)
                    yield field
                    break

        # Append fields that are not ordered
        for field in fields:
            if field.getName() not in yielded:
                yield field

    def schema(self):
        """ Schema
        """
        ctype = getattr(self.context, '.schema', None)
        schema = getattr(ctype, 'Schema', lambda: None)
        schema = schema()

        if not schema:
            return

        fields = schema.fields()
        storage = queryAdapter(self.context, IStorage)
        order = storage.order if storage else []
        fields = self.reorder(fields, order)

        if not schema:
            return

        for field in fields:
            # Skip some fields
            if field.getName() == 'id':
                continue

            # Skip invisible fields
            visible = getattr(field.widget, 'visible', None)
            if isinstance(visible, (bool, int)):
                if not visible:
                    continue
            elif isinstance(visible, dict):
                if visible.get('edit', u'visible') != u'visible':
                    continue

            yield field

    @property
    def field(self):
        """ Field
        """
        if self._field is None or isinstance(self._field, (str, unicode)):
            for field in self.schema():
                if field.getName() == self._field:
                    self._field = field
                    break
        return self._field

    def view(self, field=None):
        """ Widget view
        """
        if field:
            self._field = field
        ctype = getattr(self.context, '.schema', None)
        widget = queryMultiAdapter((ctype, self.request),
                                    name=u'progressbar.widget.view')
        widget.setPrefix(self.field.getName())
        widget.label = self.field.widget.label
        widget.field = self.field
        return widget

    def edit(self, field=None):
        """ Widget edit
        """
        if field:
            self._field = field
        ctype = getattr(self.context, '.schema', None)
        widget = queryMultiAdapter((ctype, self.request),
                                    name=u'progressbar.widget.edit')
        widget.setPrefix(self.field.getName())
        widget.field = self.field
        return widget

    def controlpanel(self, field=None):
        """ Widget preview and edit form to be listed within control panel
        """
        if field:
            self._field = field
        cpanel = queryMultiAdapter((self.context, self.request),
                                    name=u'view.metadata')
        return cpanel(field=self.field)

    def edit_reorder(self, **kwargs):
        """ Reorder fields
        """
        form = self.request.form
        form.update(kwargs)

        order = form.get('order', [])
        storage = queryAdapter(self.context, IStorage)
        storage.reorder(order)

        if form.get('ajax', False):
            return _('Items reordered')
        self.request.response.redirect(self.context.absolute_url())

    def edit_reset(self, **kwargs):
        """ Reorder fields
        """
        form = self.request.form
        form.update(kwargs)

        storage = queryAdapter(self.context, IStorage)
        storage.delete_fields()

        if form.get('ajax', False):
            return _('Reset complete')
        self.request.response.redirect(self.context.absolute_url())

    def __call__(self, *args, **kwargs):
        form = self.request.form
        form.update(kwargs)
        self._field = form.get('field', None)
        return self.index()

class ContentTypeImport(ContentType):
    """ Import settings from XML
    """
    def _redirect(self, msg='', to=''):
        """ Set status message and redirect
        """
        if not to:
            to = self.context.absolute_url()
        if msg:
            IStatusMessage(self.request).addStatusMessage(str(msg), type='info')
        self.request.response.redirect(to)

    def import_xml(self, **kwargs):
        """ Export
        """
        upload_file = kwargs.get('import_file', None)
        if getattr(upload_file, 'read', None):
            upload_file = upload_file.read()
        xml = upload_file or ''
        if not xml.startswith('<?xml version="1.0"'):
            return _('Please provide a valid xml file')

        environ = SnapshotImportContext(self.context, 'utf-8')
        importer = queryMultiAdapter((self.context, environ), IBody,
                                      name='metadata.progress.xml')
        importer.body = xml
        return None

    def __call__(self, *args, **kwargs):
        if self.request.method != 'POST':
            return  self.index()

        form = self.request.form
        form.update(kwargs)
        error = self.import_xml(**form)

        if error:
            to = self.__name__
            msg = error
        else:
            to = ''
            msg = _('Configuration imported sucesfully')

        return self._redirect(msg=msg, to=to)

class ContentTypeExport(ContentType):
    """ Export settings to XML
    """
    def export_xml(self):
        """ Export
        """
        environ = SnapshotExportContext(self.context, 'utf-8')
        export = queryMultiAdapter((self.context, environ), IBody,
                                      name='metadata.progress.xml')

        return export.body

    def __call__(self, *args, **kwargs):
        self.request.response.setHeader(
            'content-type', 'text/xml; charset=utf-8')
        self.request.response.addHeader(
            "content-disposition","attachment; filename=%s.xml" % (
                self.context.getId(),))
        return self.export_xml()
