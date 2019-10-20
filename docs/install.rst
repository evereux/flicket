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

Zip Package
~~~~~~~~~~~

Download `Flicket Dist.zip <https://github.com/evereux/flicket/tree/master/dist>`_
and unzip.


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

1. Create your database and a database user that will access the flicket
   database.


.. _SQLAlchemy_documentation: http://docs.sqlalchemy.org/en/latest/core/engines.html

2. If you are using a database server other than MySQL you should change the
   db_type value within `config.py`. See SQLAlchemy_documentation_ for options.


3. Create the configuration json file::

    python -m scripts.create_json


4. Initialise the database using manage.py from the command line::

    python manage.py db upgrade

6. Run the set-up script:. This is required to create the Admin user and site url defaults.
   These can be changed again via the admin panel once you log in::

    python manage.py run_set_up

7. Running development server for testing::

    python manage.py runserver


Log into the server using the username `admin` and the password defined during
the setup process.
