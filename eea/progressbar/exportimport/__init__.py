""" GenericSetup export/import XML adapters
"""
import os
from zope.component import queryMultiAdapter
from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.interfaces import IBody
from eea.progressbar.config import PROGRESSFILE
#
# Workflow progress
#
def importWorkflowProgress(context):
    """Import settings."""
    logger = context.getLogger('eea.progressbar')

    body = context.readDataFile(PROGRESSFILE)
    if body is None:
        logger.info("Nothing to import")
        return

    site = context.getSite()
    tool = getToolByName(site, 'portal_workflow', None)
    if not tool:
        logger.info('portal_workflows tool missing')
        return

    importer = queryMultiAdapter((tool, context), IBody, name=PROGRESSFILE)
    if importer is None:
        logger.warning("Import adapter missing.")
        return

    # set filename on importer so that syntax errors can be reported properly
    subdir = getattr(context, '_profile_path', '')
    importer.filename = os.path.join(subdir, PROGRESSFILE)

    importer.body = body
    logger.info("Imported.")

def exportWorkflowProgress(context):
    """Export settings."""
    logger = context.getLogger('eea.progressbar')
    site = context.getSite()
    tool = getToolByName(site, 'portal_workflow')

    if tool is None:
        logger.info("Nothing to export")
        return

    exporter = queryMultiAdapter((tool, context), IBody, name=PROGRESSFILE)
    if exporter is None:
        logger.warning("Export adapter missing.")
        return

    context.writeDataFile(PROGRESSFILE,
                          exporter.body, exporter.mime_type)
    logger.info("Exported.")
#
# Progress Tool
#
def importProgressTool(context):
    """Import settings."""
    logger = context.getLogger('eea.progressbar')

    body = context.readDataFile('progressbar.xml')
    if body is None:
        logger.info("Nothing to import")
        return

    site = context.getSite()
    tool = getToolByName(site, 'portal_progress', None)
    if not tool:
        logger.info('portal_progress tool missing')
        return

    importer = queryMultiAdapter((tool, context), IBody)
    if importer is None:
        logger.warning("Import adapter missing.")
        return

    # set filename on importer so that syntax errors can be reported properly
    subdir = getattr(context, '_profile_path', '')
    importer.filename = os.path.join(subdir, 'progressbar.xml')

    importer.body = body
    logger.info("Imported.")

def exportProgressTool(context):
    """Export settings."""
    logger = context.getLogger('eea.progressbar')
    site = context.getSite()
    tool = getToolByName(site, 'portal_progress')

    if tool is None:
        logger.info("Nothing to export")
        return

    exporter = queryMultiAdapter((tool, context), IBody)
    if exporter is None:
        logger.warning("Export adapter missing.")
        return

    context.writeDataFile('progressbar.xml',
                          exporter.body, exporter.mime_type)
    logger.info("Exported.")
