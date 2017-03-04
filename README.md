# Flicket

## Why Flicket?
I could not find a simple ticketing system written in python / flask. 
Also, I wanted a project to further my python / flask knowledge and development. 

If you already have a flask driven website hopefully this project is structured
in such a way that makes integrating Flicket not too much of a chore.

## Flicket Requirements
* Python 3.5.2 - I have not tested earlier versions of Python 3.
* SQL Database server

     Out of the box Flicket is configured to work with MySQL. But there 
     should be no reason other SQLAlchemy supported databases won't work
     just as well. See initial set-up for further information.
  
* See requirements.txt for python package requirements. Run `pip install requirements.txt` to install.
* This will run on either Linux or Windows. 
    
    Flask-Misaka will not pip install on Linux without `libffi-dev` .To solve this
    n Ubuntu you would type `sudo apt-get install libffi-dev`.
    
    Flask-Misaka will not pip install on windows without Microsoft Studio C++ 
    installed (an ~4GB download).


# Initial Set Up
1. Create your database and a database user that will access the flicket
database.
2. If you are using a database server other than MySQL you can easily 
switch to that by editing the db_type value. See [SQLAlchemy documentation](http://docs.sqlalchemy.org/en/latest/core/engines.html) 
for options.
3. Install the python module requirements as defined in requirements.txt. 
Best practise is to set-up a virtual environment. Once done run `pip install -r requirements.txt`
4. Create the configuration json file.
    ```
    (my-env) $ python scripts/create_json.py
    ```
4. Initialise the database using manage.py from the command line:
    ```
    (my-env) $ python manage.py db init
    (my-env) $ python manage.py db migrate
    (my-env) $ python manage.py db upgrade
    ```
5. Run the set-up script:
    ```
    (my-env) $ python manage.py run_set_up
    ```
5. Running development server for testing:
    ```
    (my-env) $ python manage.py runserver
    ```
    
