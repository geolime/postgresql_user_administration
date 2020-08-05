# -*- coding: utf-8 -*-
"""
Table specific Write Access for a user
Created on Wed Oct 18 10:58 2017
Last Updated: 2017-12-19
@author: Leif Holmquist

This script gives write access to a specified user to specified tables.
The user will be prompted in the command prompt.
The user must input the username of the user to gain write access.
The user must input the name of the schema where the tables are located.
(Only one schema per instance of this script.)
The user must input the number of tables to give access to.
The user must input the names of the tables to give access to (the user will
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
    userName = input("Please input username to give write access to the table(s): ") # User to be given access
    print("Specified user: %s\n" % userName)

    schemaName = input("Please input the schema name: ") # Schema name

    # Gives basic read access to the schema
    cur.execute('GRANT USAGE ON SCHEMA %s TO %s;' % (schemaName, userName))
    conn.commit
    cur.execute('GRANT SELECT ON ALL TABLES IN SCHEMA %s TO %s;' % (schemaName, userName))
    conn.commit
    cur.execute('GRANT SELECT ON ALL SEQUENCES IN SCHEMA %s TO %s;' % (schemaName, userName))

# Error check
except psycopg2.Error as f:
    print ("User not granted privileges to the schema!")
    #print f
    print (f.pgcode)
    print (f.pgerror)
    print ("Press Enter to exit...")
    input()

try:
    numbTable = int(input("How many tables would you like to give the user access to?: ")) # Number of tables to give access
    # Loop to give read and write access to specified tables
    counter = 0
    while numbTable > counter:
        tableName = input("Enter the table to give access to: ")
        cur.execute('GRANT ALL PRIVILEGES ON %s.%s TO %s;' % (schemaName, tableName, userName))
        conn.commit()
        print ("User granted all privileges to Schema %s Table %s.\n" % (schemaName, tableName))
        counter += 1

    # Closes database connection
    conn.close()
    print ("Database Connection Closed!\n")
    input("Press Enter to exit...")

# Error check
except psycopg2.Error as f:
    print ("User not granted privileges to all tables!")
    #print f
    print (f.pgcode)
    print (f.pgerror)
    print ("Press Enter to exit...")
    input()
