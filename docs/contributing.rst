============
Contributing
============

Contributions are welcome, preferably via pull request. Check the github issues and
project `Roadmap`_ to see what needs work. If you're thinking about adding a new
feature, it's worth opening a new ticket to check it's not already being worked on
elsewhere.


Installing
==========

The easiest way to work on Powerwiki is to fork the project on github, then use
docker compose to create the environments::

    cp docker-compose.dev.yml.default docker-compose.dev.yml
    docker-compose -f docker-compose.dev.yml up postgres
    docker-compose -f docker-compose.dev.yml up backend
    docker-compose -f docker-compose.dev.yml up frontend


Run these in separate terminals to run PostgreSQL, Django, and Webpack in development
mode with HMR.


Building JavaScript
===================

Because this is a reusable project, we distribute built frontend resources. To build::

    docker-compose -f docker-compose.dev.yml run -e FRONTEND_MODE=build frontend


Testing
=======

It is greatly appreciated when contributions come with unit tests.

Use ``pytest`` to run the tests on your current installation, or ``tox`` to run it on
the supported variants::

  pytest
  tox

These will also generate a ``coverage`` HTML report.


Roadmap
=======

* Wiki and access management
* Support for a full history and drafts
* Migration tools for moving from other wikis
