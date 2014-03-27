================
EEA Progress Bar
================
.. image:: http://ci.eionet.europa.eu/job/eea.progressbar-www/badge/icon
  :target: http://ci.eionet.europa.eu/job/eea.progressbar-www/lastBuild
.. image:: http://ci.eionet.europa.eu/job/eea.progressbar-plone4/badge/icon
  :target: http://ci.eionet.europa.eu/job/eea.progressbar-plone4/lastBuild

A system that visually display a *workflow percentage bar* or a
*workflow steps trail* in the publishing process of a document according with
the workflow state in which the document is. It also define editing progress
(document completion) of an item with customizable labels per field.

.. image:: http://eea.github.io/_images/eea.progressbar.cover.png
   :target: http://www.youtube.com/watch?v=a_U0tmw-4As&list=PLVPSQz7ahsBwUHixUt_s0kh-vaik_NCtO&feature=share

Contents
========

.. contents::

Main features
=============

- Visually display *editing progress (document completion)* of an item.
- Visually display a workflow *percentage bar/steps trail* in the publishing
  process of a document according with the workflow state in which the
  document is.
- Visually display a computed workflow *percentage bar* for Collections
  according with the children / query results items progress
- Visually display workflow *percentage bars* for items within Collection
  tabular view
- Possibility to hide/exclude certain states in progress bar (by default
  hide all states with defined percentage lower than/equal 0, configurable via
  Site Setup > Progress Bar Settings)

Install
=======

- Add eea.progressbar to your eggs section in your buildout and re-run buildout.
  You can download a sample buildout from
  https://github.com/eea/eea.progressbar/tree/master/buildouts/plone4
- Install *EEA Progress Bar* within Site Setup > Add-ons

Getting started
===============

1. Go to *ZMI > portal_workflows > Contents Tab* and select your workflow
2. Click on *Progress monitoring Tab* and update *% done* for each state
3. Go to Plone Site > Working space and add a Progress bar portlet
4. Or add a Collection, add Progress column for tabular view and enable tabular
   view for this Collection.
5. Or go to *Site Setup > Progress Bar Settings > Edit* and enable Progress Bar
   viewlets for your content-types.
6. Go to *Site Setup > Progress Bar Settings > Edit* and *Enable metadata
   progress viewlet* for Page; Go to *Site Setup > Progress Bar Settings >
   Document* and customize your *document completion* strategy for this
   content-type and then see it in action within a Page.

Dependencies
============
- plone.app.collection >= 1.0.11
- eea.jquery >= 7.7
- eea.icons

Source code
===========

- Latest source code (Plone 4 compatible):
  https://github.com/eea/eea.progressbar

Live demos
==========

- `Editing progress <http://www.youtube.com/watch?v=awS6zW2Iigo&list=PLVPSQz7ahsBwUHixUt_s0kh-vaik_NCtO&feature=share&index=1>`_
- `Workflow Steps and Workflow percentage bar <http://www.youtube.com/watch?v=a_U0tmw-4As&list=PLVPSQz7ahsBwUHixUt_s0kh-vaik_NCtO&feature=share>`_

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
