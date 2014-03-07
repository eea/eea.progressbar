""" Various setup
"""
import logging
from Products.CMFCore.utils import getToolByName
from eea.progressbar.config import TOPICMETADATA

logger = logging.getLogger('eea.progressbar')

def setupVarious(context):
    """ Do some various setup.
    """
    if context.readDataFile('eea.progressbar.txt') is None:
        return

    site = context.getSite()

    # Portal tool
    tool = getToolByName(site, 'portal_progress')
    tool.title = 'Progress Bar Settings'
    tool.unindexObject()

    # Collection
    atool = getToolByName(context, 'portal_atct')
    if not atool:
        return

    if TOPICMETADATA not in atool.topic_metadata:
        logger.info('Adding topic metadata %s within portal_atct',
                    TOPICMETADATA)
        atool.addMetadata(TOPICMETADATA, friendlyName='Progress',
                          enabled=True)
