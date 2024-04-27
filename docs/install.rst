.. _installation:

Installation
============

First read :ref:`requirements`.

It is good practise to create a virtual environment before installing
the python package requirements. Virtual environments can be
considered a sand boxed python installation for a specific application.
They are used since one application may require a different version of
a python module than another.


Getting Flicket
---------------

The source code for Flicket is hosted at GitHub. You can either get
the latest frozen zip file or use the latest master branch.


.. WARNING::
    If you are upgrading from a previous version please read the CHANGELOG.


Master Branch
~~~~~~~~~~~~~

Get the latest master branch from github using git::

    git clone https://github.com/evereux/flicket.git

Alternatively, download and unzip the master branch `zip file <https://github.com/evereux/flicket/archive/master.zip>`_.


Installing Python Requirements
------------------------------

Install the requirements using pip:::

    (env) C:\<folder_path>\flicket> pip install -r requirements.txt


Set Up
------

1. If using PostgreSQL or MySQL create your database and a database user that
   will access the flicket database. If using SQLite you can skip this step.

.. _SQLAlchemy_documentation: http://docs.sqlalchemy.org/en/latest/core/engines.html

   See SQLAlchemy_documentation_ for options.

2. Create the configuration json file::

    python -m scripts.create_json

3. If you aren't using SQLite edit `config.json` and change "db_driver".
   "null" should be replaced by the driver you are using. See the
   documentation above regarding engines, dialects and drivers. For example,
   if you are using a MySQL database and want to use the pymysql driver. ::

    "db_driver: "pymysql"

4. Install the driver you are using if not using SQLite. For example if you are
   using a MySQL database and want to use the pymysql driver. ::

    pip install pymysql

5. Upgrade the database by running the following from the command line::

    flask db upgrade

6. Run the set-up script:. This is required to create the Admin user and site url defaults.
   These can be changed again via the admin panel once you log in::

    flask run-set-up

7. Running development server for testing::

    flask run


Log into the server using the username `admin` and the password defined during
the setup process.
