# postgresql_user_administration
Python scripted Postgresql user administration commands

This is a repository of postgresql user administration commands that can be ran in either Python shell or the Command environment.

Various administration scripts:

Create Superuser - This script creates a superuser account that gives all read and write access
to the database.

Create Group - This script is to to be utilized for creating read only group roles.
  
Create Group w/ Schema specific restrictions - This script creates a group with read only access and further specifies any schema tha the user wishes to have revoked access to.

Create user - This script creates a new user with restrictions based on the assigned group role policy. This is typically read-only.

Schema Access - This script gives write access to the specified user to specified schemas.

Table Access - This script gives write access to the specified user to specified tables.

Revoke Access - This script revokes all access to the database for a user (if the wish is to not remove the user completely).

Remove User - This script completely removes the user from their dependencies and drops the user from the database entirely.
