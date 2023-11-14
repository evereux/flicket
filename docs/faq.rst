=============
Flicket - FAQ
=============

What is Flicket?
----------------

Flicket is a simple open source ticketing system driven by the python
flask web micro framework.

Flicket also uses the following python packages:

    alembic, bcrypt, flask-admin, flask-babel, flask-login, flask-migrate,
    flask-principal, flask-sqlalchemy, flask-script, flask-wtf, jinja2,
    Markdown, WTForms

See `README.rst` for full requirements.

## Licensing

For licensing see `LICENSE.md`

Tickets
-------

General
~~~~~~~~~~~
1. How do I create a ticket?

   Select 'create ticket' from the Flicket pull down menu.

2. How do I assign a ticket?

   Scenario: You have raised a ticket and you know to whom the ticket
   should be assigned.

   Navigate to [flicket home page](/flicket/) and select the ticket you
   wish to assign. Within the ticket page is a button to `assign` ticket.

3. How do I release a ticket?

   Scenario: You have been assigned a ticket but the ticket isn't your
   responsibility to complete or you are unable to for another reason.

   Navigate to [flicket home page](/flicket/) and select the ticket to
   which you have been assigned. Within the ticket page is a button
   to `release` the ticket from your ticket list.

4. How do I close a ticket?

   Scenario: The ticket has been resolved to your satisfaction and you
   want to close the ticket.

   Navigate to [flicket home page](/flicket/) and select the ticket
   which you would like to close. Within the ticket page is a button
   to `replay and close` the ticket.

   Only the following persons can close a ticket:
   * Administrators.
   * The user which has been assigned the ticket.
   * The original creator of the ticket.

    You may `claim` the ticket so that you may close it.

5. What is markdown?

    Markdown is a lightweight markup language with plain text formatting syntax.

    The text contents of a ticket can be made easier to read by employing
    markdown syntax.

6. How do I change the locale (language settings)?

    In the top right hand corner click on your profile and select `User Details`.
    Within the `Edit User Details` page you can pick your locale. Locales can
    also be set on user creation.

    If you'd like to add a new locale see the section `Adding Additional Languages`.


Searching
~~~~~~~~~

The ticket main page can be filtered to show only results of a specific
interest to you. Tickets can be filtered by department, category, user
and a text string.


Departments
~~~~~~~~~~~

.. note::
    Only administrators or super users can add / edit or delete departments.

1. How do I add new departments?

   Navigate to Departments via the menu bar and use the add departments form.

2. How do I edit departments?

   Navigate to [departments](/flicket/departments/) and select the edit
   link against the department name.

3. How do I delete departments?

   Navigate to [departments](/flicket/departments/) and select the remove
   link against the department name. This is represented with a cross.


Categories
~~~~~~~~~~

.. note::
    Only administrators or super users can add / edit or delete categories.

1. How do I add categories?

   Navigate to [departments](/flicket/departments/) and select the link
   to add categories against the appropriate department name.

1. How do I edit categories?

   Navigate to [departments](/flicket/departments/) and select the link
   to add categories against the appropriate department name.