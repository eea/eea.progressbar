""" Events
"""
from logging import getLogger
logger = getLogger('eea.progressbar')
from zope.component import  queryAdapter
from eea.progressbar.interfaces import IStorage

def add_schema(obj, event):
    """ Add schema object
    """
    try:
        ctype = obj.getField('ctype').getAccessor(obj)()
        if not ctype:
            return

        oid = '.schema'
        if oid not in obj.objectIds():
            oid = obj.invokeFactory(ctype, id=oid)
            res_obj = obj[oid]
            fields = res_obj.schema.fields()
            storage = queryAdapter(obj, IStorage)
            for field in fields:
                storage.add_field(field.getName())
        obj[oid].unindexObject()
    except Exception, err:
        logger.exception(err)
