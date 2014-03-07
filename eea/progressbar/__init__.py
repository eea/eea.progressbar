""" Initialize
"""
from eea.progressbar import zmi

def initialize(context):
    """Initializer called when used as a Zope 2 product."""

    from eea.progressbar import content
    content.initialize(context)

zmi.initialize()
