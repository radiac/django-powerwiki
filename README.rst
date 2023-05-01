===============================================
Django Powerwiki - Run multiple wikis in Django
===============================================

A work in progress wiki system for Django 2.2+ on Python 3.7+.

* Project site: http://radiac.net/projects/django-powerwiki/
* Source code: https://github.com/radiac/django-powerwiki

.. image:: https://github.com/radiac/django-powerwiki/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/radiac/django-powerwiki/actions/workflows/ci.yml

.. image:: https://codecov.io/gh/radiac/django-powerwiki/branch/develop/graph/badge.svg?token=5VZNPABZ7E
    :target: https://codecov.io/gh/radiac/django-powerwiki


Features
========

* Run one or multiple wikis from one installation
* Full control over who can read and edit content, by user or group
* Create pages in Markdown, reStructuredText, plain text, or extend with a custom format
* Syntax highlighting using CodeMirror
* Flexible responsive layout
* In-document navigation, full text search, assets support and more

See `Upgrading <docs/upgrading.rst>`_ for changelog and upgrade instructions


Quickstart
==========

#. Install in a single or multiple wiki configuration in your existing Django site - see
   `Installation <docs/installation.rst>`_

#. Add users, wikis and configure permissions in the admin site

#. Write pages using your choice of markup language - see `Usage <docs/usage.rst>`_
