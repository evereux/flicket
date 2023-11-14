Flicket
=======

Flicket is a simple web based ticketing system written in Python using
the flask web framework which supports English and French locales. Additional
locales can be added by following the section `Adding Additional Languages`
within this README.


Documentation
-------------

For documentation and screenshots please visit: https://flicket.readthedocs.io/en/latest/


Upgrading From Earlier Versions
-------------------------------

See the changelog for changes and additional steps to take when upgrading.


Requirements
------------
Prior to installing and running Flicket please read these requirements.

* Python =>3.90

* SQL Database server with JSON support (for example PostgreSQL >=9.2,
  MySQL >=5.7, MariaDB >=10.2, SQLite >=3.9)


Production Environment
----------------------

To serve Flicket within a production environment webservers such as Apache
or nginx are typically used. See the documentation for how to install Apache
on Windows.
