# -*- coding: utf-8 -*-
"""
Revoke all Database Access for a user
Created on Wed Oct 18 14:43 2017
Last Updated: 2017-12-19
@author: Leif Holmquist

This script revokes access to a specified user to the database.
The user will be prompted in the command prompt.
The user must input the username of the user whom shall be revoked all
access to the database.

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
    dbName = "postgres" # Database name
    adminName = "postgres_w" # Superuser name
    adminPass = "postgres17" # Superuser password
    hostIp = "161.52.9.139" # Host IP
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
    # Required Input

    userName = input("Please enter the username to revoke all access to the database: ") # # User to be revoked access
    print("Specified user: %s\n" % userName)

    # Revokes user from access to the database
    cur.execute('REVOKE CONNECT ON DATABASE %s FROM %s;' % (dbName, userName))
    conn.commit()
    print ("User %s revoked access from %s database.\n" % (userName, dbName))

    # Closes database connection
    conn.close()
    print ("Database Connection Closed!\n")
    input("Press Enter to exit...")

# Error check
except psycopg2.Error as f:
    print ("User NOT revoked from accessing the database!")
    #print f
    print (f.pgcode)
    print (f.pgerror)
    print ("Press Enter to exit...")
    input()
