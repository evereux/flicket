# Changelog

# 0.1.7
*   Added view 'my_tickets'.
*   Added links to ticket views filtered by department on main page.
*   Refactored ticket views methods and placed in FlicketTicket model.

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