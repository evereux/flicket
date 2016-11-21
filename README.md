# Flicket

## Why Flicket?
I couldn't find a simple ticketing system written in python / flask to
easily integrate within my current intranet work environment. Also, needed
a project to tackle to further my python / flask developement. There are 
several very good open source options out there but they felt like overkill.

If you already have a flask drive website hopefully this project is structured
in such a way that makes merging this into that not too much of a chore.

## Caveats
I'm no programmer or web designer. Test first.

## Flicket Requirements
* Python 3.5.2 - I developed this application using this version of python.
* MySQL Database server
     Out of the box Flicket is configured to work with MySQL. But there 
     should be no reason other SQLAlchemy supported databases won't work
     just aswell. Switching to those is simple. See Initial Set Up.
* See requirements.txt for python package requirements.
* This will run on either Linux or Windows. But, Flask-Misaka will not pip
install on windows without Microsoft Studio C++ install (a bloody whopping
great 4GB download). I'll investigate at some point whether I can supply
a whl of this package with this application.
* The default set-up uses a MySQL connection. It should be quite possible
to also use PostgreSQL by just chaning the connection string in config.py.


# Initial Set Up
1. Create your database and a database user that will access the flicket
database. See `config.py` for the defaults.
2. Edit config.py username password defaults. Especially the password default!
3. If you are using a database server other than MySQL you can easily 
switch to that by editing the db_type value. See SQLAlchemy documentation 
for options.
4. Install the python module requirements as defined in requirements.txt. 
Best practise is to set-up a virtual environment and do `pip install -r requirements.txt`
5. Initialise the database using alembic from the command line:
    alembic revision --autogenerate -m "initialise database"
    alembic upgrade head
    


