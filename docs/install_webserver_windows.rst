======================
Installing A Webserver
======================

Currently the documentation will only describe how to install and configure
the Apache webserver on Windows since this can be a bit trickier than on Linux.
However, some of the steps here can also be used in Linux.

The instructions provided are for use with Python and Apache. You must ensure
both Python and Apache have been compiled with the same version of Visual
Studio. Also, Python and Apache must both be compiled for the same CPU
architecture (x86 x64).

Also, the paths defined in this guide can be changed. You can by all means use
different paths but you should try and and get the webserver running with the
settings defined herein first.


Apache - Windows
----------------
Prior to installing a webserver you should confirm that flicket is working
correctly by running the developement webserver as described in the
:ref:`installation` instructions.


Install mod_wsgi
~~~~~~~~~~~~~~~~

Download the applicable `mod_wsgi` whl for your flavour of Apache and Python
from  the `Unofficial Windows Binaries for Python Extension Packages <https://www.lfd.uci.edu/~gohlke/pythonlibs/#mod_wsgi>`_
page. For example, if you have `Python 3.6 x64` and `Apache 2.4 x64` you
would get the whl `mod_wsgi-4.6.5+ap24vc14-cp36-cp36m-win_amd64.whl`.

Whilst **active in your flicket virtual environment** install `mod_wsgi`::

    pip install <path_to_download>mod_wsgi-4.6.5+ap24vc14-cp36-cp36m-win_amd64.whl


Installing Apache
~~~~~~~~~~~~~~~~~

Download Apache compiled with VC14 from the `apache lounge <https://www.apachelounge.com/download/VC14/>`_.

Unzip the apache folder to your `c:\\` directory. You should end up with a
folder structure like this::

    C:\Apache24
        C:\Apache24\bin
        C:\Apache24\cgi-bin
        ...

Open the file `C:\Apache24\conf\httpd.conf` in a text editor like
`notepad++ <https://notepad-plus-plus.org/>`_.

Modify the following line to read the following::

    SRVROOT "C:\Apache24"

Add the following lines (put these after the other LoadModule declarations)::

    LoadModule wsgi_module "<path_to_your_virtualenv>/lib/site-packages/mod_wsgi/server/mod_wsgi.cp36-win_amd64.pyd"
    WSGIPythonHome "<path_to_your_virtualenv>"

Uncomment the vhosts line::

    Include conf/extra/httpd-vhosts.conf

Uncomment mod_version line

    LoadModule version_module modules/mod_version.so

Edit the file `C:\Apache24\conf\extra\httpd-vhosts.conf`.

Comment out the existing configurations lines by prefixing with a # (good
reference for future troubleshooting).

Add the following::

    <VirtualHost *:8000>

        ServerName <ip_address or hostname>
        ServerAlias <ip_address or hostname>
        ServerAdmin <your_email@there.com>

        DocumentRoot C:\Apache24\htdocs

        <Directory C:\Apache24\htdocs>
        <IfVersion < 2.4>
            Order allow,deny
            Allow from all
        </IfVersion>
        <IfVersion >= 2.4>
            Require all granted
        </IfVersion>
        </Directory>

        WSGIScriptAlias / <path_to_flicket>run.wsgi

        <Directory <path_to_flicket>>
        <IfVersion < 2.4>
            Order allow,deny
            Allow from all
        </IfVersion>
        <IfVersion >= 2.4>
            Require all granted
        </IfVersion>
        </Directory>

    </VirtualHost>

Edit the file `run.wsgi` so that the path points to your Flicket virtual environment.

Register Apache As A Service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Navigate to the Apache folder and register the service with name `Apache HTTP Server`::

    cd "C:\Apache24\bin"
    httpd.exe -k install -n "Apache HTTP Server"

Start Apache
~~~~~~~~~~~~

To start the service use either Windows Serivce Manage and start the service
`Apache HTTP Server` or from the command prompt whilst in the folder `c:\Apache24\bin`::

    httpd -k start -n "Apache HTTP Server"

Flicket should now be available in your browser by accessing http:\\<ip_address or hostname>:8000

Troubleshooting
~~~~~~~~~~~~~~~

To troubleshoot problems starting the apache service or accessing the webpage
you should start by reading your Apache installations log files normally located in `c:\Apache24\logs`.

