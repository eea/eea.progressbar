""" Doc tests
"""
import doctest
import unittest
from eea.progressbar.tests.base import FUNCTIONAL_TESTING
from plone.testing import layered

OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)

def test_suite():
    """ Suite
    """
    suite = unittest.TestSuite()
    suite.addTests([
        layered(
            doctest.DocFileSuite(
                'interfaces.py',
                optionflags=OPTIONFLAGS,
                package='eea.progressbar'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'content/interfaces.py',
                optionflags=OPTIONFLAGS,
                package='eea.progressbar'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'controlpanel/interfaces.py',
                optionflags=OPTIONFLAGS,
                package='eea.progressbar'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'widgets/interfaces.py',
                optionflags=OPTIONFLAGS,
                package='eea.progressbar'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'storage/interfaces.py',
                optionflags=OPTIONFLAGS,
                package='eea.progressbar'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'widgets/simple/interfaces.py',
                optionflags=OPTIONFLAGS,
                package='eea.progressbar'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'docs/exportimport.txt',
                optionflags=OPTIONFLAGS,
                package='eea.progressbar'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'README.txt',
                optionflags=OPTIONFLAGS,
                package='eea.progressbar'),
            layer=FUNCTIONAL_TESTING),
    ])
    return suite
