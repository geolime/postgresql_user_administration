# -*- coding: utf-8 -*-
"""
Create a Superuser (Automatic read and write access)
Created on Wed Oct 18 09:15 2017
Last Updated: 2017-12-19
@author: Leif Holmquist

This script creates a superuser account that gives all read and write access
to the database.
The user will be prompted in the command prompt.
The user must input the name of the superuser.
The user must input the password of the superuser.

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
    conn = psycopg2.connect(dbname=dbName, user=adminName, host=hostIp, password=adminPass, port=portNumb)
    print ("Database Connected!\n")

# Error check
except psycopg2.Error as e:
    print ("Unable to connect to the Database.\n")
    print (e)
    #print (e.pgcode)
    #print (e.pgerror)
    #print (traceback.format_exc())

cur = conn.cursor()
try:
    # Required input
    userName = input("Enter desired superuser name: ") # Superuser name to be created
    print ("Username: su_%s" % userName)
    passWord = input("Enter desired superuser password: ")
    print ("Password: %s" % passWord) # Superuser password to be created

    validity = input("Should this user have an expiry time? (y/n): ")

    if validity in ("y", "Y", "Yes", "yes"):
        validTime = input("Please enter date when this user should expire (yyyy-mm-dd): ")
        print ("User valid until: %s" % validTime)
    else:
        validTime = 'infinity'

    # Creates superuser account
    #createUser = "CREATE ROLE %s WITH LOGIN PASSWORD '%s' SUPERUSER INHERIT CREATEDB CREATEROLE REPLICATION VALID UNTIL '%s';" % (userName, passWord, validTime)
    cur.execute("""CREATE ROLE su_%s WITH LOGIN PASSWORD '%s' SUPERUSER INHERIT CREATEDB CREATEROLE REPLICATION VALID UNTIL '%s';""" % (userName, passWord, validTime))
    conn.commit()
    print ("Superuser su_%s Created!\n" % userName)

    # Closes database connection
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
