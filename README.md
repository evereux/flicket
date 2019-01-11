# Flicket

## What is Flicket
Flicket is a simple web based ticketing system written in Python using the flask web framework.

## Why Flicket?
I could not find a simple ticketing system written in python / flask or any other language that I really liked.
Also, I wanted a project to further my python / flask knowledge and development. 

## Requirements
Prior to installing and running Flicket please read these requirements.
* Python =>3.5 - I have not tested earlier versions of Python 3.
* SQL Database server

     Out of the box Flicket is configured to work with MySQL. But there 
     should be no reason other SQLAlchemy supported databases won't work
     just as well. See initial set-up for further information.
  

* This will run on either Linux or Windows. Mac is untested but there should be no issues.

* See requirements.txt for python package requirements. Run `pip install requirements.txt` to install.


# Initial Set Up
1. Create your database and a database user that will access the flicket
database.
2. If you are using a database server other than MySQL you should change the  
db_type value within `config.py`. 
See [SQLAlchemy documentation](http://docs.sqlalchemy.org/en/latest/core/engines.html) 
for options.
3. Install the python module requirements as defined in requirements.txt. 
Best practise is to set-up a virtual environment. Once done run `pip install -r requirements.txt`
4. Create the configuration json file.
    ```
    (my-env) $ python scripts/create_json.py
    ```
    or on windows
    ```
    (my-env) C:\path_to_project> python scripts\create_json.py
    ```
4. Initialise the database using manage.py from the command line:
    ```
    (my-env) $ python manage.py db init
    (my-env) $ python manage.py db migrate
    (my-env) $ python manage.py db upgrade
    ```
5. Run the set-up script:. This is required to create the Admin user and site url defaults.
   These can be changed again via the admin panel once you log in.
    ```
    (my-env) $ python manage.py run_set_up
    ```
5. Running development server for testing:
    ```
    (my-env) $ python manage.py runserver
    ```
    Log into the server using the username `admin` and the password
    defined during the setup process.
    
# Production Environment

To serve Flicket within a production environment webservers such as Apache
or nginx are typically used.

# Exporting / Importing Flicket Users
## Exporting
If you need to export the users from the Flicket database you can run the following command:
    ```
    (my-env) $ python manage.py export_users
    ```
    
This will output a json file formatted thus:
    ```
    [{'username': 'jblogs', name: 'Joe Blogs', email:'jblogs@email.com', 'password': 'bcrypt_encoded_string'}]
    ```
## Importing
If you need to import users run the following command:
    ```
    (my-env) $ python manage.py import_users
    ```
The file has to formatted as shown in the Exporting example.

