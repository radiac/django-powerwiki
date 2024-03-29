===============
Using Powerwiki
===============

Working with pages
==================

Add a page
----------

To add a page, create a link to a page that doesn't exist (or visit it directly by
changing the URL).

Links to pages that don't exist will be style differently; going to the page will take
you to the edit form (provided you have permission).


Delete a page
-------------

Remove all content from a page and save it to delete it.


Syntax
======

Powerwiki supports markup engines for writing in different source languages. You can add
your own engine too if there's another language you would like to support. Set the
default language with the ``POWERWIKI_MARKUP_ENGINE`` setting, and override it by wiki
and page.


Wiki syntax links
-----------------

The easiest way to link to pages and assets is using the custom wiki syntax. This is
available in all markup engines.

To link to a page in the same wiki::

    [[path]]
    [[path|label]]
    [[wiki:path]]
    [[:slug:path]]


To link to a page in another wiki::

    [[wiki:wiki_slug:path]]


To link to an asset::

    [[asset:path]]


To insert an asset as an image::

    [[image:path]]


To insert an index table (list of child pages) for the current page::

    [[index:]]

To insert an index table for another page in the same wiki::

    [[index:path]]


Native links
------------

The engines adds URL schemes ``wiki:`` and ``asset:`` to add explicit links to pages and
assets. These urls will always be relative to the wiki root.

Relational links to wiki pages will be treated as ``wiki:`` links, but relative to the
current page rather than wiki root.

Wiki slugs must start with an alphanumeric character and can only contain letters,
numbers and dashes.

Page paths can be arranged in a hierarchy with ``/``, but each slug must start with an
alphanumeric character. Asset names must also start with an alphanumeric character. Page
paths and asset names have no other restrictions.

Examples on a page ``animals/cats``::

    <a href=":path">...</a>
    <a href="wiki:path">...</a>


Inter-wiki links::

    <a href=":slug:path">...</a>
    <a href="wiki:slug:path">...</a>


Assets::

    <img src="asset:name">


reStructuredText
----------------

Normally reStructuredText slugifies links by stripping whitespace, for example::

    `Using Powerwiki`_
    # becomes
    <a href="usingpowerwiki">UsingPowerwiki</a>

Powerwiki prefers to slugify using dashes, so adds two custom roles to the rst parser::

    :wiki:`Using Powerwiki'_
    # becomes
    <a href="using-powerwiki">Using Powerwiki</a>

and for assets::

    :asset:`Using Powerwiki'_
    # becomes
    <a href="asset:using-powerwiki">Using Powerwiki</a>
