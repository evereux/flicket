.. _requirements:

Requirements
============

Operating System
----------------

This will run on either Linux or Windows. Mac is untested.


Python
------
Python =>3.9.



SQL Database Server
-------------------

Out of the box Flicket is configured to work with `MySQL <https://www.mysql.com/downloads/>`_. But there
should be no reason other SQLAlchemy supported databases won't work
just as well.

.. note::

    When I last tried SQLite I had problems configuring the email settings
    within the administration settings. You may have to change them manually
    within SQLite.


Web Server
----------

For a production environment a webserver such as `Apache <https://httpd.apache.org/>`_
or `nginx <https://www.nginx.com/>`_ should be used to serve the application.
