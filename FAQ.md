
# Flicket - FAQ

## What is Flicket?

Flicket is a simple open source ticketing system driven by the python flask 
web framework. 

Flicket also uses the following python packages:

    alembic, bcrypt, flask-admin, flask-login, flask-principal, flask-sqlalchemy, flask-wtf, jinja2, misaka, WTForms
    
See `README.md` for full requirements.

## Licensing
For licensing see `LICENSE.md`

## SetUp

For set-up instructions see `README.md` available on github.

## Tickets

### General

1. How do I create a ticket?

   Navigate to [flicket home page](/flicket/) and press the 
   'create ticket' button. This will take you to form to create a new 
   ticket.
   
2. How do I assign a ticket?

   You have raised a ticket and you know to whom the ticket should be 
   assigned.

   Navigate to [flicket home page](/flicket/) and select the ticket you 
   wish to assign. Within the ticket page is a button to `assign` ticket.
   
3. How do I release a ticket?

   You've been assigned a ticket but the ticket isn't your repsonsibility
   to complete or you are unable to for another reason.
   
   Navgiate to [flicket home page](/flicket/) and select the ticket to
   which you have been assigned. Within the ticket page is a button
   to `release` the ticket from your ticket list.
   
4. How do I close a ticket?

   The ticket has been resolved satifactorily and you want to close the ticket.
   
   Navgiate to [flicket home page](/flicket/) and select the ticket
   which you would like to close. Within the ticket page is a button
   to `close` the ticket.
   
   Only the following persons can close a ticket:
   * Administrators.
   * The user which has been assigned the ticket.
   * The original creator of the ticket.
   
### Searching

1. What are quick filters?

   Quick filters are simply buttons that enable you to quick filter tickets
   by department, category and status.

2. What does the search box search?

   The search box searches ticket title, content and replies for your 
   text string.

## <a name="permissions"></a>Permissions

1. Some actions within Flicket required permission levels. If you don't 
   require an action that requires elevated permissions you should raise
   a ticket and assign the ticket to the appropriate user.

## Departments

1. How do add new departments?

   Navigate to [departments](/flicket/departments/) and use the add 
   departments form.
   
   Please note this action requires elevated access. See [Permissions](#permissions)
   
2. How do I edit departments?

   Navigate to [departments](/flicket/departments/) and select the edit
   link against the department name.
   
   Please note this action requires elevated access. See [Permissions](#permissions) 
   
3. How do I delete departments?

   Navigate to [departments](/flicket/departments/) and select the remove
   link against the department name. This is represented with a cross.
   
   Please note this action requires elevated access. See [Permissions](#permissions)

## Categories

1. How do I add categories?
    
   Navigate to [departments](/flicket/departments/) and select the link
   to add categories against the appropriate department name.
   
  Please note this action requires elevated access. See [Permissions](#permissions)
   
1. How do I edit categories?
    
   Navigate to [departments](/flicket/departments/) and select the link
   to add categories against the appropriate department name.
   
   Please note this action requires elevated access. See [Permissions](#permissions)