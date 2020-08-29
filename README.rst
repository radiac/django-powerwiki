===============================================
Django Powerwiki - Run multiple wikis in Django
===============================================

A work in progress wiki system for Django 2.2+


Features
========

* Run one or multiple wikis from one installation
* Full control over who can read and edit content, by user or group
* Create pages in markdown or restructured text

See `Upgrading <docs/upgrading.rst>`_ for changelog and upgrade instructions


Installation
============

1. Install ``django-powerwiki`` (currently only on github)::

    pip install -e git+https://github.com/radiac/django-powerwiki.git#egg=django-powerwiki


2. Add to ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...
        'powerwiki',
    )

3.  Link to urls.py

    * To install a single wiki change your settings for ``POWERWIKI_SINGLE_MODE`` and
      ``POWERWIKI_SINGLE_NAME``
    * If you want to use a custom URL structure, remember to check UPGRADES in the
      future for notice of changes to ``urls.py``
    * The front page of the wiki app will always be ``index`` - if you
      are running in single wiki mode, that will be the front page of the wiki,
      or in multi wiki mode it will be the list of available wikis.

    Example::

        path('wiki/', include('powerwiki.urls', namespace='powerwiki')),

4.  Templates

    * Expects your site ``base.html`` to have ``title``, ``css`` and ``content``
      blocks.


Using powerwiki
===============

Writing pages
-------------

Powerwiki supports markup engines for writing in different source languages. You can add
your own engine too if there's another language you would like to support. Set the
default language with the ``POWERWIKI_MARKUP_ENGINE`` setting, and override it by wiki
and page.

The engines adds URL schemes ``wiki:`` and ``asset:`` to add explicit links to pages and
assets. These urls will always be relative to the wiki root.

Relational links to wiki pages will be treated as ``wiki:`` links, but relative to the
current page rather than wiki root.

Page paths can be arranged in a hierarchy with ``/``, but each slug must start with an
alphanumeric character.

Examples on a page ``animals/cats``::

    <a href=":path">...</a>
    <a href="wiki:path">...</a>


Inter-wiki links::

    <a href=":slug:path">...</a>
    <a href="wiki:slug:path">...</a>


Assets::

    <img src="asset:slug">
