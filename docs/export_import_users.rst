Exporting / Importing Flicket Users
-------------------------------------
Exporting
~~~~~~~~~
If you need to export the users from the Flicket database you can run the
following command:

    python manage.py export_users


This will output a json file formatted thus:

.. code-block:: python

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

    python manage.py import_users

The file has to formatted as shown in the Exporting example.

