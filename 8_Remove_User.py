# -*- coding: utf-8 -*-
"""
Remove a user's access to the database and delete the user
Created on Wed Oct 18 09:15 2017
Last Updated: 2017-12-19
@author: Leif Holmquist

This script removes the user's access to the database. This script also removes
all dependencies the user owns and deletes the user.
The user will be prompted in the command prompt.
The user must input the name of the user to be deleted.

If something is wrong with the connection, please check the following inputs
contained within the script:
dbName
adminName
adminPass
hostIp
portNumb

"""

# load the adapter
import sys
import psycopg2
import traceback

# load the psycopg extras module
import psycopg2.extras

try:
    # Input variables
    dbName = "" # Database name
    adminName = "" # Superuser name
    adminPass = "" # Superuser password
    hostIp = "" # Host IP
    portNumb = 5432 # Port number, default


    # Connects to the database
    conn = psycopg2.connect(dbname=dbName, user=adminName, host=hostIp, password=adminPass,port=portNumb)
    print ("Database Connected!\n")

# Error check
except psycopg2.Error as e:
    print ("Unable to connect to the Database.\n")
    print (e)
    #print (e.pgcode)
    #print (e.pgerror)
    #print (traceback.format_exc())
    print ("Press Enter to exit...")
    input()

cur = conn.cursor()
try:
    # Required input
    userName = input("Enter the username to be removed from the database: ") # User to be removed
    userCheck = input("You have specified user: %s. Continue? (y/n) " % userName)

    if userCheck in ("y", "Y", "Yes", "yes"):
        # Drops the users dependencies
        cur.execute('DROP OWNED BY %s;' % (userName))
        conn.commit()
        print("User dependencies dropped!\n")

        # Delete the user
        cur.execute('DROP USER %s;' % (userName))
        conn.commit()
        print("User %s has been deleted from the database.\n" % userName)
    else:
        pass

    conn.close()
    print ("Database Connection Closed!\n")
    input("Press ENTER to exit...")

# Error check
except psycopg2.Error as f:
    print ("User can't be created!")
    #print f
    print (f.pgcode)
    print (f.pgerror)
    print ("Press Enter to exit...")
    input()
