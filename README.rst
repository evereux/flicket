Flicket
=======

Flicket is a simple web based ticketing system written in Python using
the flask web framework which supports English and French locales. Additional
locales can be added by following the section `Adding Additional Languages`
within this README.


Why Flicket?
---------------
I could not find a simple ticketing system written in python / flask or
any other language that I really liked. Also, I wanted a project to
further my python / flask knowledge and development.


Can I See It Working?
---------------------
I have a working version at: https://flicket.evereux.uk/. If you'd like access
drop an email to me at evereux@gmail.com. Tell me username / email you would
like to use.

Currently, all the views require login so I'll have to up account for you
until I create a better hopefully spam proof version.


Screenshots
-----------

.. image:: screenshots/01_home_page_2019-05-12_16-23-44.png
    :width: 50pt


Upgrading From Earlier Versions
-------------------------------

See the changelog for changes and additional steps to take when upgrading.


Requirements
------------
Prior to installing and running Flicket please read these requirements.

* Python =>3.5 - I have not tested earlier versions of Python 3.

* SQL Database server
    Out of the box Flicket is configured to work with MySQL. But there
    should be no reason other SQLAlchemy supported databases won't work
    just as well. See initial set-up for further information.

    When I last tried SQLite I had problems configuring the email settings
    within the administration settings. You may have to change them manually
    within SQLite.


* This will run on either Linux or Windows. Mac is untested.

* See `requirements.txt` for python package requirements. Run `pip install requirements.txt` to install.


Initial Set Up
----------------

1. Create your database and a database user that will access the flicket
database.

.. _SQLAlchemy_documentation: http://docs.sqlalchemy.org/en/latest/core/engines.html

2. If you are using a database server other than MySQL you should change the
db_type value within `config.py`. See SQLAlchemy_documentation_
for options.

3. Install the python module requirements as defined in requirements.txt.
Best practise is to set-up a virtual environment. Once done run `pip install -r requirements.txt`

4. Create the configuration json file.

.. code-block::

    (my-env) $ python scripts/create_json.py

or on windows

.. code-block::

    (my-env) C:\path_to_project> python scripts\create_json.py


5. Initialise the database using manage.py from the command line:

.. code-block::

    (my-env) $ python manage.py db init
    (my-env) $ python manage.py db migrate
    (my-env) $ python manage.py db upgrade

6. Run the set-up script:. This is required to create the Admin user and site url defaults.
   These can be changed again via the admin panel once you log in.

.. code-block::

    (my-env) $ python manage.py run_set_up

6. Running development server for testing:

.. code-block::

    (my-env) $ python manage.py runserver


Log into the server using the username `admin` and the password defined during
the setup process.


Production Environment
----------------------

To serve Flicket within a production environment webservers such as Apache
or nginx are typically used.


Windows NT Authentication
-------------------------

If enabled in the administration config settings (use_auth_domain, auth_domain)
Flicket can authenticate users on the domain upon which Flicket is running. This means
that users don't have to be manually added.

You will also need to install pywin32.




Exporting / Importing Flicket Users
-------------------------------------
Exporting
~~~~~~~~~
If you need to export the users from the Flicket database you can run the
following command:

.. code-block::

    (my-env) $ python manage.py export_users

    
This will output a json file formatted thus:

.. code-block::

    [
        {
            'username': 'jblogs',
            'name': 'Joe Blogs',
            'email':'jblogs@email.com',
            'password': 'bcrypt_encoded_string'
        }
    ]


Importing
~~~~~~~~~
If you need to import users run the following command:

.. code-block::

    (my-env) $ python manage.py import_users


The file has to formatted as shown in the Exporting example.


Adding Additional Languages
---------------------------

Flicket now supports additional languages through the use of Flask Babel.
To add an additional local:

* Edit `SUPPORTED_LANGUAGES` in `config.py` and add an additional entry to
  the dictionary. For example: `{'en': 'English', 'fr': 'Francais',
  'de': 'German'}`


* Whilst in the project root directory you now need to initialise
  the new language to generate a template file for it.

.. code-block::

    pybabel init -i messages.pot -d application\translations -l de


* In the folder `application\translations` there should now be a new folder
  `de`.


* Edit the file `messages.po` in that folder. For example:

.. code-block::

    msgid "403 Error - Forbidden"
    msgstr "403 Error - Verboten"


* Compile the translations for use:

.. code-block::

    pybabel compile -d application\translations


* If any python or html text strings have been newly tagged for translation
  run:

.. code-block::

    pybabel extract -F babel.cfg -o messages.pot .


* To get the new translations added to the .po files:

.. code-block::

    pybabel update -i messages.pot -d application\translations
