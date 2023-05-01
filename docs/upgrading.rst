=================
Powerwiki Changes
=================

Changelog
=========

0.4.0, 2023-05-01
-----------------

Features:

* In-document navigation sidebar (requires JavaScript)
* Enhanced search when using postgresql
* Ability to search multiple wikis at once
* New ``[[index:<path>]]`` tag
* Converts ``->`` into ``→``


Changes:

* New ``Page.depth`` value, requires migration
* Internal API: renamed ``WIKILINK_`` constants to ``TAG_``
* Removed support for Python <3.9 - may still work, no longer tested


0.3.1, 2021-02-20
-----------------

Bugfix:

* Relax path and asset validation rules


0.3.0, 2021-02-20
-----------------

Features:

* Add CodeMirror v5
* Add post-engine processing for ``[[..]]`` wiki links
* reStructuredText markup engine now supports ``:wiki:`` and ``:asset:`` roles for
  slugification consistent with the rest of Powerwiki
* Missing pages and assets are styled differently


Changes:

* Removed support for Python <3.7


Bugfix:

* Emptying a page's contents will delete it
* Cross-wiki linking no longer leaks page paths
* Missing assets no longer cause errors


0.2.2, 2020-12-20
-----------------

Bugfix:

* Correct index template


0.2.1, 2020-09-05
-----------------

Changed:

* Test fixes


0.2.0, 2020-09-05
-----------------

Features:

* Added option to select language


Changed:

* Removed support for Django <2.2
* Updated templates and replaced JS and CSS
* Added example project


0.1.0, 2014-04-25
-----------------

Features:

* Support for multiple wikis with access control
