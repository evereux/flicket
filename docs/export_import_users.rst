Exporting / Importing Flicket Users
-------------------------------------
Exporting
~~~~~~~~~
If you need to export the users from the Flicket database you can run the
following command:

    flask export-users-to-json


This will output a json file in the same folder called `users.json` formatted thus:

.. code-block:: python

    [
        {
            "username": "jblogs",
            "name": "Joe Blogs",
            "email": "jblogs@email.com',
            "password": "bcrypt_encoded_string"
        }
    ]

To get the bcrypt encoded string of the password you can use the function `hash_password` in
`application.flicket.scripts.hash_password`.

Importing
~~~~~~~~~
If you need to import users run the following command:

    flask import-users-from-json

The file has to formatted as shown in the Exporting example and the filename shall be `users.json`.



