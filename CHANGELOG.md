# Changelog

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