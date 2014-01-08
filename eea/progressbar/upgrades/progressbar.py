""" eea.progressbar upgrades
"""
from Products.CMFCore.utils import getToolByName


def add_icons(context):
    """We will depend on eea.icons for our Workflow Steps Trail Progress Bar.
    """
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile('profile-eea.icons:default')
