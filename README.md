# Flicket Set-Up

## Why Flicket?
I couldn't find a simple ticketing system written in python / flask to
easily integrate within my current intranet work environment. Also, needed
a project to tackle to further my python / flask developement. There are 
several very good open source options out there but they felt like overkill.

## Caveats
I'm no programmer or web designer. Test first.

## Flicket Requirements
* Python 3.5.2
     I suspect versions < Python 3.5 will work but I have not tested them.
* MySQL Database server
     Out of the box Flicket is configured to work with MySQL. But there 
     should be no reason other SQLAlchemy supported databases won't work
     just aswell.
* See requirements.txt for python package requirements.
* This will run on either Linux or Windows. But, Flask-Misaka will not pip
install on windows without Microsoft Studio C++ install (a bloody whopping
great 4GB download). I'll investigate at some point whether I can supply
a whl of this package with this application.
* The default set-up uses a MySQL connection. It should be quite possible
to also use PostgreSQL by just chaning the connection string in config.py.


# Initial Set Up
* Login to Flicket and change the flicket admin password.
* Delete setup.py from root folder


