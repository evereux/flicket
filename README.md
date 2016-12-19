# Flicket

## Why Flicket?
I couldn't find a simple ticketing system written in python / flask. 
Also, I wanted a project to further my python / flask knowledge and development. 

If you already have a flask driven website hopefully this project is structured
in such a way that makes integrating Flicket not too much of a chore.

## Flicket Requirements
* Python 3.5.2 - I have not tested earlier versions but I suspect they will 
work aswell (not 3< though)
* SQL Database server

     Out of the box Flicket is configured to work with MySQL. But there 
     should be no reason other SQLAlchemy supported databases won't work
     just aswell. See initial set-up for further information.
* See requirements.txt for python package requirements.
* This will run on either Linux or Windows. But, Flask-Misaka will not pip
install on windows without Microsoft Studio C++ installed (a bloody whopping
great 4GB download). I'll investigate at some point whether there are licensing 
restrictions stopping me from supplying a whl compiled for windows.


# Initial Set Up
1. Create your database and a database user that will access the flicket
database.
2. Edit config.py username password defaults for your admin and database users. 
3. Do __not__ leave the password defaults as is.
4. If you are using a database server other than MySQL you can easily 
switch to that by editing the db_type value. See [SQLAlchemy documentation](http://docs.sqlalchemy.org/en/latest/core/engines.html) 
for options.
5. Install the python module requirements as defined in requirements.txt. 
Best practise is to set-up a virtual environment and do `pip install -r requirements.txt`
6. Initialise the database using alembic from the command line:
    alembic revision --autogenerate -m "initialise database"
    alembic upgrade head
    
