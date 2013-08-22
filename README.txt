================
EEA Progress Bar
================
.. image:: http://ci.eionet.europa.eu/job/eea.progressbar-www/badge/icon
  :target: http://ci.eionet.europa.eu/job/eea.progressbar-www/lastBuild
.. image:: http://ci.eionet.europa.eu/job/eea.progressbar-plone4/badge/icon
  :target: http://ci.eionet.europa.eu/job/eea.progressbar-plone4/lastBuild

A system that visually display a progress bar in the publishing process of a
document according with the workflow state in which the document is.

Contents
========

.. contents::

Main features
=============

- Visually display a progress bar in the publishing process of a document
  according with the workflow state in which the document is.
- Visually display a computed progress bar for Collections according with
  the children / query results items progress
- Visually display progress bars for items within Collection tabular view

Install
=======

- Add eea.progressbar to your eggs section in your buildout and re-run buildout.
  You can download a sample buildout from
  https://github.com/eea/eea.progressbar/tree/master/buildouts/plone4
- Install eea.progressbar within Site Setup > Add-ons

Getting started
===============

1. Go to *ZMI > portal_workflows > Contents Tab* and select your workflow
2. Click on *Progress monitoring Tab* and update *% done* for each state
3. Go to Plone Site > Working space and add a Progress bar portlet
4. Or add a Collection, add Progress column for tabular view and enable tabular
   view for this Collection.

Dependencies
============
- plone.app.collection >= 1.0.11

Source code
===========

- Latest source code (Plone 4 compatible):
  https://github.com/eea/eea.progressbar


Copyright and license
=====================
The Initial Owner of the Original Code is European Environment Agency (EEA).
All Rights Reserved.

The EEA Progress Bar (the Original Code) is free software;
you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation;
either version 2 of the License, or (at your option) any later
version.

More details under docs/License.txt


Funding
=======

EEA_ - European Environment Agency (EU)

.. _EEA: http://www.eea.europa.eu/
