=================================
Django Uzewiki - Wikis for Django
=================================

An advanced Wiki system for Django


Features
========

* Run one or multiple wikis from one installation
* Full control over who can read and edit content, by user or group
* Chose from a variety of markup languages
* Support for a full history and drafts
* Migration tools for moving from other wikis

Version 0.0.1

* See `CHANGES <CHANGES>`_ for full changelog and roadmap
* See `UPGRADE <UPGRADE.rst>`_ for how to upgrade from earlier releases


Requirements
============

These packages are required:

* Django >= 1.3
* django-timewarp

These packages are optional:

* pretext

It is recommended that you use ``South`` to manage schema migrations, as future
versions of Yarr will need changes to the database.


Installation
============

1. Install ``django-uzewiki`` (currently only on github)::

    pip install -e git+https://github.com/radiac/django-uzewiki.git#egg=django-uzewiki

2. Add to ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...
        'uzewiki',
    )

3. Link to urls.py

  * To install a single wiki change your settings for ``UZEWIKI_SINGLE`` and
    ``UZEWIKI_SINGLE_NAME``
  * If you want to use a custom URL structure, remember to check UPGRADES in the
    future for notice of changes to ``urls.py``
  * The front page of the wiki app will always be ``uzewiki-index`` - if you
    are running in single wiki mode, that will be the front page of the wiki,
    or in multi wiki mode it will be the list of available wikis.

4. Templates
  * Expects your site ``base.html`` to have ``title``, ``css`` and ``content``
    blocks.


Migrating from other wiki engines
=================================

From dokuwiki
-------------

* Create a folder on the same machine as your django installation, eg ``~/tmp/mywiki``
* Copy the ``data/pages`` directory into ``mywiki`` as ``mywiki/pages``
* Copy the ``data/media`` directory into ``mywiki`` as ``mywiki/assets``
* Run ``python manage.py convert_wiki dokuwiki <path/to/mywiki>``
  * This will move ``start.txt`` files to convert from dokuwiki namespaces
  * It will make a basic attempt to convert from dokuwiki syntax to pretext,
    using regular expressions. It's pretty simplistic, and will get things
    wrong (ie it will break a link with a label in a table). It would be nice
    to think that at some point this would be replaced with a proper dokuwiki
    parser, but there are no concrete plans to do so at this time.
* Zip ``mywiki`` as ``mywiki.zip``
* Create a wiki on your django site and import ``mywiki.zip``
* Manually fix any issues in the dokuwiki markup

Notes
=====

* To edit a page, add /edit/ to it
  * Front page is a little different - go to /UZEWIKI_FRONT/edit/


Credits
=======

Thanks to all contributors, who are listed in CHANGES.
