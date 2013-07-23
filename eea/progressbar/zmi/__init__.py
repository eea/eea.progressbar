""" Progress monitoring
"""
from Products.DCWorkflow.States import StateDefinition
from Products.DCWorkflow.DCWorkflow import DCWorkflowDefinition

def extendState(context):
    """ State tabs
    """
    options = StateDefinition.manage_options
    for option in options:
        if option['action'] == 'manage_progress':
            return
    StateDefinition.manage_options += (
        {'label': 'Progress monitoring', 'action': 'manage_progress'},
    )

def extendWorkflow(conttext):
    """ Workflow tabs
    """
    options = DCWorkflowDefinition.manage_options
    for option in options:
        if option['action'] == 'manage_progress':
            return
    DCWorkflowDefinition.manage_options += (
        {'label': 'Progress monitoring', 'action': 'manage_progress'},
    )

def initialize(context=None):
    """ Zope2 initialize
    """
    extendState(context)
    extendWorkflow(context)
