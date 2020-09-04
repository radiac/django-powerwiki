===============
Using Powerwiki
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
