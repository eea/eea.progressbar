""" Initialize
"""
def initialize(context):
    """Initializer called when used as a Zope 2 product."""

    from eea.progressbar import content
    content.initialize(context)
