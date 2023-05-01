============
Installation
============

#. Install ``django-powerwiki`` (currently only on github)::

    pip install -e git+https://github.com/radiac/django-powerwiki.git#egg=django-powerwiki


#. Add to ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...
        "powerwiki",
    )

   If you're using postgresql, also add ``"django.contrib.postgres"`` for full text
   search support.


#. Configure, for example::

    POWERWIKI_MARKUP_ENGINES = [
        "powerwiki.markup.rest.RestructuredText",
        "myproject.markup.Wikimedia",
    ]
    POWERWIKI_SINGLE_MODE = True

    See `Configuration <configuration>`_ below for all configuration options.


#.  Add the project to your ``urls.py``, for example::

        path('wiki/', include('powerwiki.urls', namespace='powerwiki')),


#.  Configure your templates and styles so Powerwiki can render what it needs to.

    Powerwiki expects your site ``base.html`` to have ``title``, ``css`` and ``content``
    blocks.

    See `Templates`_ for more details.


Configuration
=============

``POWERWIKI_SINGLE_MODE``
    If ``True``, run in single wiki mode - no wiki slugs, the top level url will be the
    index page of the wiki.

    If ``False``, run in multiple wiki mode - wiki slugs, the top level url will be a
    list of available wikis.

    Default is multiple wiki mode::

        POWERWIKI_SINGLE_MODE = False


``POWERWIKI_SINGLE_SLUG``
    In single wiki mode, this is the slug given to the wiki internally. This will be
    used in the url if the wiki ever moves to multiple wikis, otherwise it is not used.

    Default::

        POWERWIKI_SINGLE_SLUG = "default"


``POWERWIKI_PERM_INDEX``
    Permission for who can see the wiki index page in multiple wiki mode.

    This should be one of the permission constants in ``powerwiki.constants``:

    * ``PERM_SU`` - Superusers only
    * ``PERM_STAFF`` - Staff and superusers
    * ``PERM_USERS`` - Users, staff and superusers
    * ``PERM_PUBLIC`` - Everyone

    Default::

        from powerwiki.constants import PERM_PUBLIC
        POWERWIKI_PERM_INDEX = PERM_PUBLIC


``POWERWIKI_FRONT_PATH``
    Path for the front page of the wiki. Used internally, and used for linking to the
    named page. You will normally not need to change this.

    Default::

        POWERWIKI_FRONT_PATH = "index"


``POWERWIKI_LINK_TAGS``
    List of tag and attribute pairs to look for wiki links.

    Default::

        POWERWIKI_LINK_TAGS = [
            ("a", "href"),
            ("img", "src"),
        ]


``POWERWIKI_MARKUP_ENGINES``
    List of paths to markup engine classes.

    Default::

        POWERWIKI_MARKUP_ENGINES = [
            "powerwiki.markup.rest.RestructuredText",
            "powerwiki.markup.md.Markdown",
            "powerwiki.markup.plain.PlainText",
        ]


``POWERWIKI_MARKUP_ENGINE_DEFAULT``
    Default markup engine to use. Must be listed in ``POWERWIKI_MARKUP_ENGINES``.

    Default::

        POWERWIKI_MARKUP_ENGINE_DEFAULT = "powerwiki.markup.rest.RestructuredText"


``POWERWIKI_HTML_PARSER``
    HTML parser for BeautifulSoup. The default is the most supported, but there are
    faster parsers available if installed - see BeautifulSoup docs for more details.

    Default::

        POWERWIKI_HTML_ENGINE = "html.parser"


Templates
=========

See the example project for a suggestion of how to set up your templates.

Powerwiki templates inherit from ``templates/powerwiki/base.html``, which in turn
inherits from ``templates/base.html``.

They expect the base template to use the following variables:

``{{ title }}``
    The page title. Should be used in the head ``<title>`` tag, and shown at the top of
    the page body.

``{{ body_class }}``
    A class name to add to the ``<body>`` tag based on the current page.


The base template should also provide the following blocks:

``{% block js %}{% endblock %}``
    Insert powerwiki JavaScript into the page.

``{% block css %}{% endblock %}``
    Insert powerwiki CSS into the page. This provides layout only.

    The parent container of the ``content`` block should be styled to the full width and
    height of the viewport.


``{% block content %}{% endblock %}``
    Insert the page content.


The base template should also render messages from Django's messaging framework, e.g.::

    {% for message in messages %}
    <p>{{ message|safe }}</p>
    {% endfor %}


Styles
======

The included stylesheet is largely for page layout and unopinionated about design. It
will attempt to create full-height elements for some pages, so the ``content`` block
should be styled to use as much width and height of the viewport as is possible within
your design, eg with ``min-height: 100%`` or vertical flexbox. See the example project
for details.

There are some values you may want to override to fit with your design, such as
``.powerwiki__content`` padding, or ``.powerwiki__content a[data-missing=True]`` style -
see stylesheets for details.
