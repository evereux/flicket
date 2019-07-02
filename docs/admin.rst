.. _admin:

Administration
==============

Command Line Options
--------------------

From the command line the following options are available.

.. module:: flicket_admin

.. sourcecode::

    python manage.py

    usage: manage.py [-?]
                     {db,run_set_up,export_users,import_users,update_user_posts,update_user_assigned,email_outstanding_tickets,runserver,shell}
                     ...

    positional arguments:
      {db,run_set_up,export_users,import_users,update_user_posts,update_user_assigned,email_outstanding_tickets,runserver,shell}
        db                  Perform database migrations
        run_set_up
        export_users        Command used by manage.py to export all the users from
                            the database to a json file. Useful if we need a list
                            of users to import into other applications.
        import_users        Command used by manage.py to import users from a json
                            file formatted such: [ { username, name, email,
                            password. ]
        update_user_posts   Command used by manage.py to update the users total
                            post count. Use when upgrading from 0.1.4.
        update_user_assigned
                            Command used by manage.py to update the users total
                            post count. Use if upgrading to 0.1.7.
        email_outstanding_tickets
                            Script to be run independently of the webserver.
                            Script emails users a list of outstanding tickets that
                            they have created or been assigned. To be run on a
                            regular basis using a cron job or similar. Email
                            functionality has to be enabled.
        runserver           Runs the Flask development server i.e. app.run()
        shell               Runs a Python shell inside Flask application context.

    optional arguments:
      -?, --help            show this help message and exit



Administration Config Panel
---------------------------

Options
~~~~~~~

For email configuration the following options are available. At a minimum you should configure `mail_server`,
`mail_port`, `mail_username` and `mail_password`.

For more information regarding these settings see the documentation for Flask-Mail.

.. autoclass:: flicket_admin.models.flicket_config.FlicketConfig
    :members:
