# Changelog

If you are migrating from any earlier version you should ensure:
       * you upgrade the database. 
    ~~~
    python manage.py db migrate
    python manage.py db upgrade
    ~~~

# 0.1.9 - in developement.
*   Expanded API functionality ... still work to be done during this release
*   Fixed issue where field contents were not remembered after a search.
*   Added command to send emails to users who have tickets not closed. This needs to be invoked from the command line
    using `python manage.py email_outstanding_tickets` using a (weekly? don't spam your users too much!") cron job or 
    similar.
*   Fixed user not being able to edit own ticket (replies were OK).
*   The assignee can now close the ticket.
*   Ticket priority can now be changed during reply. Submitting reply and close will overwrite selection to closed.
*   Status changes now logged.
*   Started documentation.
*   Removed FAQ link from Flicket. Now controlled by documentation.
*   Added markdown help and removed link to external reference.
*   Documentation. 


# 0.1.8
*   Upgraded SQLAlchemy and Jinja2 due to security warnings.
*   Updated wording of prompts in 'populate_database_with_junk.py'.
*   Added admin setting so the page banner title can be changed from 'Flicket'.
*   Merged pull request: https://github.com/evereux/flicket/pull/20
*   Added ability to export tickets view as an excel file. Very project manager friendly, I believe.
*   Added authentication method for nt machines. Requires pywin32 to be installed.
    If Flicket is running on an NT (windows) machine and pywin32 is installed it will try to authenticate the user
    on that machine if they aren't already registered.
    I will add LDAP authentication at some point soon when I can find a means to test (OpenLDAP hasn't worked for me.)
*   Added a default group "super_user". super_users's can create departments and categories but can't access the 
    administration settings or delete topics or posts.

    If you are migrating from any earlier version you should ensure:
       * you upgrade the database. 
    ~~~
    python manage.py db migrate
    python manage.py db upgrade
    ~~~
    
        * add the user super_user to the groups in flicket_admin/groups/ groups page. You can use the admin 
        configuration area to do this.
    

# 0.1.7
*   Added view 'my_tickets'.
*   Added links to ticket views filtered by department on main page.
*   Refactored ticket views methods and placed in FlicketTicket model.
*   Moved ticket creation and editing from views to own class.
*   Total assigned now stored in users details and not calculated on the fly.

    If you are migrating from any earlier version you should ensure you upgrade
    the database. 
    ~~~
    python manage.py db migrate
    python manage.py db upgrade
    ~~~    
    
    Also, manually update your users total_posts count whilst site
    is offline. This can be done by running `python manage.py update_user_assigned`
*   Added missing showmarkdown toggle to reply form.
*   populate_database_with_junk.py now uses mimesis for random data generation.
*   Change README to rst format and various wording changes.
*   Added flask-babel support.
*   Added French locale option. Thanks to SolvingCurves.


## 0.1.6a
*   various bug fixes.
*   user can now change status when replying to ticket.

## 0.1.5a
*   Changed dependancy from Flask-Misaka to the python library Markdown.
    This is because installing Flask-Misaka on Windows is too many hoops
    to jump through.

*   A number of package updates made to requirements. See requirements.txt.

*   The total number of posts is now stored in the user table instead of manually
    calculated. This is due to slow page loading times (users page) for large
    databases.
    
    If you are migrating from any earlier version you should ensure you upgrade
    the database. Also, manually update your users total_posts count whilst site
    is offline. This can be done by running `python manage.py update_user_posts`
    
 *  Some minor text updates to flash notifications.