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
                            Emails users a list of outstanding tickets that
                            they have created or been assigned. This now runs
                            daily at 09:00 via the Celery beat schedule (see
                            "Celery Status" below) and can also be run manually
                            with this command. Email functionality has to be
                            enabled.
        runserver           Runs the Flask development server i.e. app.run()
        shell               Runs a Python shell inside Flask application context.

    optional arguments:
      -?, --help            show this help message and exit


Celery Status
-------------

The Admin Panel page `/flicket_admin/celery/` shows the state of the Celery
task queue: whether the broker is reachable, the workers that are online and
the number of tasks they are currently running.

Periodic tasks are scheduled with Celery beat:

* `email_outstanding_tickets` - daily at 09:00. Emails users of their
  outstanding tickets (see the command above).
* `delete_old_task_logs` - daily at 03:00. Deletes task log rows older than
  the configured retention period (see below).

To run a worker and beat locally: `make celery-worker` and `make celery-beat`.
Via Docker: `make docker-up` (the stack includes the `redis`, `worker` and
`beat` services).

Task Logs
---------

The Admin Panel page `/flicket_admin/task_logs/` lists every executed
background task: its name, status (`STARTED`, `SUCCESS` or `FAILURE`), when it
started, how long it took and a link to the full record. The record shows the
JSON args/kwargs the task was called with, the result on success, or the
exception on failure, plus the Celery id and the worker that ran it. A
`?status=` filter (All/Started/Success/Failure) shows just one status.

Older task logs are deleted by the daily `delete_old_task_logs` beat task. The
number of days logs are kept is the *Task log retention (days)* setting on the
Flicket Configuration panel (0 = keep forever).



Administration Config Panel
---------------------------

Options
~~~~~~~

For email configuration the following options are available. At a minimum you should configure `mail_server`,
`mail_port`, `mail_username` and `mail_password`.

For more information regarding these settings see the documentation for Flask-Mail.

.. autoclass:: flicket_admin.models.flicket_config.FlicketConfig
    :members:
