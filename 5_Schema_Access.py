# -*- coding: utf-8 -*-
"""
Schema specific Write Access to a user
Created on Wed Oct 18 11:40 2017
Last Updated: 2017-12-19
@author: Leif Holmquist

This script gives write access to a specified user to specified schemas.
The user will be prompted in the command prompt.
The user must input the username of the user to gain write access.
The user must input the number of schemas to give access to.
The user must input the names of the schemas to give access to (the user will
be prompted for each schema seperately).

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
    # Required Input
    userName = input("Please input username to give write access to the schema(s): ") # User to be given access'
    userCheck = input("You have specified user: %s. Continue? (y/n) " % userName)

    if userCheck in ("y", "Y", "Yes", "yes"):

        numbSchema = int(input("How many schemas would you like to give the user access to?: \n"))

        # Loop to give read and write access to specified schemas
        counter = 0
        while numbSchema > counter:
            schemaName = input("\nEnter the schema to give write access: ")
            cur.execute('GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA %s TO %s;' % (schemaName, userName))
            conn.commit
            print ("User granted all privileges to Schema %s.\n" % schemaName)
            counter += 1
    else:
        pass

    # Closes database connection
    conn.close()
    print ("Database Connection Closed!\n")
    input("Press Enter to exit...")

# Error check
except psycopg2.Error as f:
    print ("User not granted privileges to the schema!")
    #print (f)
    print (f.pgcode)
    print (f.pgerror)
    print ("Press Enter to exit...")
    input()
