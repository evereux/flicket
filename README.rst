Flicket
=======

Flicket is a simple, open source, web based ticketing system written in
Python using the Flask web framework. It supports English and French
locales, Markdown formatted tickets, a token authenticated REST API and,
optionally, single sign on through an OpenID Connect provider such as
`Zitadel <https://zitadel.com>`_.

For documentation and screenshots please visit:
https://flicket.readthedocs.io/en/latest/


Features
--------

* Ticket management: create, edit and delete tickets and replies; assign,
  claim, release and close tickets; change status, priority, department
  and category.
* Statuses (Open, In Work, Awaiting Information, Closed), priorities
  (low, medium, high), departments and categories are created during set up
  and can be managed from the UI.
* Markdown with live preview, file attachments (configurable allow-list of
  extensions) and user avatars.
* Ticket subscriptions and e-mail notifications for ticket creation,
  replies, assignment, release, closure, password resets and a digest of
  outstanding tickets.
* A full change history / action log per ticket and time (hours) tracking.
* Search, filter and sort tickets, CSV export, dashboard pie charts and a
  carousel of open high priority tickets.
* Users and groups (``flicket_admin`` and ``super_user``), disabled
  accounts, password reset, per-user locale and an administration panel for
  site, e-mail and upload settings (``/flicket_admin/``).
* A REST API under ``/flicket-api/`` with token authentication covering
  tickets, posts, users, departments, categories, department categories,
  priorities, statuses, subscriptions, histories, actions and uploads.
* Internationalisation via Flask-Babel (English and French out of the box).
* Optional SSO via Zitadel / OIDC: authorization code flow with PKCE,
  automatic account provisioning and single logout. Local username /
  password login remains available alongside SSO. See `Single Sign On`_.


Requirements
------------

Prior to installing and running Flicket please read these requirements.

* Python 3.10 or newer. Release 0.3.1 raised the minimum to 3.10; earlier
  Python 3 versions may still work (see ``CHANGELOG.md``).
* A SQLAlchemy supported SQL database with JSON support: SQLite >= 3.9,
  PostgreSQL >= 9.2, MySQL >= 5.7 or MariaDB >= 10.2. ``config.json``
  selects SQLite (``db_type`` = 1), PostgreSQL (2) or MySQL (3); for the
  latter two, set ``db_driver`` and install the matching driver (for
  example ``pymysql``).
* The Python packages listed in ``requirements.txt`` (Flask, SQLAlchemy,
  Flask-SQLAlchemy, Flask-Migrate, Flask-Babel, Flask-Login, Flask-Mail,
  Flask-WTF, Authlib, Plotly, ...).

For production use the application should be served by a WSGI server behind
a web server such as Apache or nginx (see `Production Environment`_).


Installation / Quick Start
--------------------------

From the project root::

    git clone https://github.com/evereux/flicket.git
    cd flicket
    python -m venv env
    . env/bin/activate            # Windows: env\Scripts\activate
    pip install -r requirements.txt

1. Create the configuration file. This is an interactive script that writes
   ``config.json`` in the project root::

       python -m scripts.create_json

   You will be asked for the database type and credentials and, optionally,
   for the Zitadel SSO settings. ``SECRET_KEY`` and the notification user
   password are generated automatically. ``config.json`` is listed in
   ``.gitignore`` - never commit it.

2. If you are not using SQLite, edit ``config.json`` and set ``db_driver``
   to the driver you are using, then install it::

       pip install pymysql

3. Create / migrate the database::

       flask db upgrade

4. Run the initial set up. This creates the ``admin`` user (you choose the
   password), the ``flicket_admin`` and ``super_user`` groups, default
   statuses, priorities, departments and categories, the internal
   notification user and the site settings. You will also be asked for the
   site base URL::

       flask run-set-up

5. Start the development server (``.flaskenv`` sets ``FLASK_APP`` and port
   5000)::

       flask run

   Log in at http://localhost:5000/ with username ``admin`` and the
   password chosen during set up, then configure e-mail and the remaining
   site settings from ``/flicket_admin/config/``.

See ``docs/install.rst`` for the full installation guide.


Development Tasks (Makefile)
----------------------------

A ``Makefile`` wraps the common tasks. Installs are incremental - the
virtualenv in ``env/`` is created once and dependencies are only
reinstalled when ``requirements*.txt`` changes. Run ``make help`` for the
full list; the most useful targets are::

    make bootstrap       # venv + dev deps + interactive config.json
    make db-upgrade      # apply migrations
    make setup           # create the admin user and default data
    make run             # dev server (make run PORT=8080 to override)
    make test            # pytest, or a smoke check when no tests/ exists
    make check           # fast syntax check of all Python sources
    make docs            # build Sphinx HTML docs into docs/_build/html
    make clean           # remove caches (keeps config.json and the database)

``PYTHON=python3.11 make install`` selects a different interpreter for the
virtualenv. The Makefile never overwrites ``config.json`` or your database.


Docker / Compose
----------------

The ``Dockerfile`` has two build targets: ``development`` (Flask dev server
with reload and the development requirements) and ``production`` (gunicorn
running as a non-root user). ``compose.yaml`` is the shared base (app +
MariaDB); ``compose.dev.yaml`` and ``compose.prod.yaml`` are overrides.
Flicket reads ``config.json`` at import time, so ``docker/entrypoint.sh``
generates it from environment variables, waits for the database and runs
``flask db upgrade`` before starting the server. It never overwrites an
existing ``config.json``.

First create ``.env`` (random ``SECRET_KEY``, database and notification
passwords are generated for you), then start the stack::

    make docker-init       # writes .env from .env.example; never overwrites
    make docker-up         # dev stack: http://localhost:5000
    make docker-setup      # interactive: creates the admin user and site URL
    make docker-logs       # follow app + db logs

``make docker-setup`` runs ``flask run-set-up`` in a TTY; it asks for the
admin e-mail/password and the site base URL. Log in as ``admin`` afterwards.

Other useful targets: ``make docker-dev`` (up + follow logs),
``make docker-prod`` (gunicorn, non-root), ``make docker-test`` /
``make docker-ci`` (pytest or an import smoke test inside the container;
run these against the dev stack, which has pytest installed),
``make docker-migrate``, ``make docker-shell``, ``make docker-down``,
``make docker-clean`` and ``make docker-reset`` (destructive: removes the
database and uploads). Run ``make help`` for the full list.

MariaDB data and the two upload folders live in named volumes
(``db-data``, ``uploads-data``, ``avatars-data``), so they survive container
recreation. The development override bind-mounts the source tree into
``/app`` for instant reloads; the production image contains a copy of the
code instead. Database credentials and ``SECRET_KEY`` come from ``.env``
(see ``.env.example``); keep ``SECRET_KEY`` stable across restarts or user
sessions will be invalidated. DB passwords must be URL-safe because the
app interpolates them into the SQLAlchemy URI. In the development stack the
source tree is bind-mounted, so the generated ``config.json`` appears in
the repository root (it is gitignored); delete it to regenerate from
``.env`` if you change any of those values.

Note that ``.flaskenv`` enables ``FLASK_DEBUG`` and is only used by the
development target; the production image removes it.


Configuration
-------------

Runtime configuration lives in ``config.json`` (generated by
``scripts/create_json.py``) and is read by ``config.py``. The most
important keys are:

* ``db_type`` - 1 = SQLite, 2 = PostgreSQL, 3 = MySQL.
* ``db_driver`` - SQLAlchemy driver for PostgreSQL / MySQL (``null`` for
  SQLite).
* ``db_username``, ``db_password``, ``db_url``, ``db_port`` - database
  connection details.
* ``db_name`` - database name, or the SQLite filename.
* ``SECRET_KEY`` - Flask session signing key (auto generated).
* ``NOTIFICATION_USER_PASSWORD`` - password of the internal notification
  user (auto generated).
* ``ZITADEL_ENABLED``, ``ZITADEL_ISSUER``, ``ZITADEL_CLIENT_ID``,
  ``ZITADEL_CLIENT_SECRET`` - optional SSO settings (see below).

Site settings that can be changed while the application is running (mail
server and credentials, base URL, posts per page, allowed upload
extensions, CSV dump limit, category change options, ...) are stored in
the database and edited from the administration panel, not in
``config.json``. Mail sending is suppressed by default after set up until
SMTP settings are configured.


Single Sign On
--------------

SSO is optional and disabled by default. Local username / password login
stays available when SSO is enabled. To turn it on, set the Zitadel keys
in ``config.json`` (``python -m scripts.create_json`` asks for them) and
restart Flicket::

    "ZITADEL_ENABLED": true,
    "ZITADEL_ISSUER": "https://id.exam-studio.com",
    "ZITADEL_CLIENT_ID": "<client id from Zitadel>",
    "ZITADEL_CLIENT_SECRET": "<client secret from Zitadel>"

In Zitadel, register a Web application with redirect URI
``<base-url>/login/sso/callback`` and post logout URI ``<base-url>/``.
Flicket discovers the OIDC endpoints from
``<ZITADEL_ISSUER>/.well-known/openid-configuration`` and uses the
authorization code flow with PKCE. Accounts are provisioned on first login
(matched by ``oidc_sub``, then by verified e-mail, otherwise created with
no groups); groups and roles remain administrator managed. Logging out of
Flicket also ends the session at the identity provider.

After enabling SSO, run ``flask db upgrade`` so the migration adds the
``oidc_sub`` column used to link accounts. When running behind a reverse
proxy, forward ``X-Forwarded-Proto`` and ``Host`` (or set the base URL via
``flask run-set-up``) so callback URLs are not downgraded from https to
http. Full details are in ``docs/sso.rst``.


Command Line (Flask CLI)
------------------------

In addition to the standard ``flask db`` migration commands,
``application/commands.py`` registers:

* ``flask run-set-up`` - initialise database defaults and the admin user.
* ``flask export-users-to-json`` / ``flask import-users-from-json`` - move
  users through a ``users.json`` file
  (see ``docs/export_import_users.rst``).
* ``flask update-total-post-count`` /
  ``flask update-total-user_assigned`` - recalculate cached user counters
  when upgrading from older releases.
* ``flask email-outstanding-tickets`` - e-mail users a list of their open
  tickets; intended for a cron job and requires working mail settings.

Run ``flask --help`` for the full list. ``application.commands`` is
registered automatically on application start up.


REST API
--------

The API is served under ``/flicket-api/`` and uses bearer tokens. Obtain a
token with your username and password, then pass it in the
``Authorization`` header::

    http --auth <username>:<password> POST http://localhost:5000/flicket-api/tokens
    http GET http://localhost:5000/flicket-api/tickets/ "Authorization: Bearer <token>"

Revoke a token with ``DELETE /flicket-api/tokens``. Endpoint references and
response formats are documented in ``docs/api.rst`` (generated from the
docstrings in ``application/flicket_api/views/``).


Adding Additional Languages
---------------------------

Flicket ships with English (``en``) and French (``fr``) translations.
Additional locales are added with Flask-Babel: add the locale to
``SUPPORTED_LANGUAGES`` in ``config.py``, then use ``pybabel`` to
initialise, translate, compile and update the message catalogues. The full
procedure is in ``docs/languages.rst`` (translation templates:
``messages.pot`` and ``babel.cfg``).


Upgrading From Earlier Versions
-------------------------------

See ``CHANGELOG.md`` for the changes and any extra steps required when
upgrading. In general, after pulling a new version::

    pip install -r requirements.txt
    flask db upgrade

Always back up your database and ``config.json`` first. SSO deployments
also need the ``oidc_sub`` migration, which is applied by ``flask db
upgrade``.


Production Environment
----------------------

Do not use ``flask run`` in production. Serve the WSGI application
(``application:app``; ``run.wsgi`` contains an Apache / mod_wsgi example
whose virtualenv path must be adjusted for your host) through a WSGI
server such as gunicorn or uWSGI behind a web server such as Apache or
nginx. ``BaseConfiguration`` sets ``DEBUG = False``; ``.flaskenv`` is
intended for development only (it enables ``FLASK_DEBUG``).

Also:

* Keep ``config.json`` and ``SECRET_KEY`` secret and out of version
  control.
* Set the site base URL (via ``flask run-set-up`` or the admin panel) so
  links in e-mails and API responses resolve correctly.
* Configure SMTP settings in ``/flicket_admin/config/``; mail sending is
  suppressed by default until you do so.
* Restrict the upload folders
  (``application/flicket/static/flicket_uploads`` and
  ``application/flicket/static/flicket_avatars``) to the extensions
  allowed in the admin panel.


Documentation
-------------

* Online: https://flicket.readthedocs.io/en/latest/
* Local Sphinx sources in ``docs/``: ``install.rst``, ``admin.rst``,
  ``sso.rst``, ``api.rst``, ``languages.rst``,
  ``export_import_users.rst``, ``faq.rst`` and ``screenshots.rst``. Build
  them with the packages in ``requirements-development.txt``.


Contributing, Security and License
----------------------------------

* Contributors: ``CONTRIBUTORS.md``
* Reporting security concerns: ``SECURITY.md``
* Todo list: ``TODO.md``
* License: ``LICENSE.md``
