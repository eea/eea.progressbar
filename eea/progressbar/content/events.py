""" Events
"""
from logging import getLogger
logger = getLogger('eea.progressbar')

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
        obj[oid].unindexObject()
    except Exception, err:
        logger.exception(err)
