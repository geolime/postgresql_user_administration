# Postgresql User Administration
Variou Python scripted Postgresql user administration commands.

This is a repository of postgresql user administration commands that can be ran in either Python shell or the Command environment.

## Various administration scripts:

### Create Superuser
This script creates a superuser account that gives all read and write access
to the database.
https://github.com/geolime/postgresql_user_administration/blob/master/1_Create_Superuser.py

### Create Group
This script is to to be utilized for creating read only group roles.
https://github.com/geolime/postgresql_user_administration/blob/master/2_Create_Group.py
  
### Create Group w/ Schema specific restrictions 
This script creates a group with read only access and further specifies any schema tha the user wishes to have revoked access to.
https://github.com/geolime/postgresql_user_administration/blob/master/2_Create_Read_Group_Revoke_Specific_Schema.py

### Create user 
This script creates a new user with restrictions based on the assigned group role policy. This is typically read-only.
https://github.com/geolime/postgresql_user_administration/blob/master/3_Create_User_Read-Only.py

### Schema Access
This script gives write access to the specified user to specified schemas.
https://github.com/geolime/postgresql_user_administration/blob/master/5_Schema_Access.py

### Table Access
This script gives write access to the specified user to specified tables.
https://github.com/geolime/postgresql_user_administration/blob/master/6_Table_Access.py

### Revoke Access 
This script revokes all access to the database for a user (if the wish is to not remove the user completely).
https://github.com/geolime/postgresql_user_administration/blob/master/7_Revoke_Access.py

### Remove User 
This script completely removes the user from their dependencies and drops the user from the database entirely.
https://github.com/geolime/postgresql_user_administration/blob/master/8_Remove_User.py
