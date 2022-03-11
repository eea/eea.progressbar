""" Installer
"""
import os
from setuptools import setup, find_packages

NAME = 'eea.progressbar'
PATH = NAME.split('.') + ['version.txt']
VERSION = open(os.path.join(*PATH)).read().strip()

setup(name=NAME,
      version=VERSION,
      description="Progress bar based on current document review_state",
      long_description_content_type="text/x-rst",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Framework :: Zope2",
          "Framework :: Plone",
          "Framework :: Plone :: 4.0",
          "Framework :: Plone :: 4.1",
          "Framework :: Plone :: 4.2",
          "Framework :: Plone :: 4.3",
          "Programming Language :: Zope",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "License :: OSI Approved :: GNU General Public License (GPL)",
      ],
      keywords='EEA progressbar Add-ons Plone Zope',
      author='European Environment Agency: IDM2 A-Team',
      author_email='eea-edw-a-team-alerts@googlegroups.com',
      url='https://github.com/collective/eea.progressbar',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['eea'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'eea.icons',
          'eea.jquery > 7.6',
          # -*- Extra requirements: -*-,
          'eea.progress.workflow',
          'eea.progress.editing'
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
