# -*- coding: utf-8 -*-
"""
Create a Read-Only Group Role with Restricted Schema Access
Created on Wed Oct 18 10:58 2017
Last Updated: 2017-12-19
@author: Leif Holmquist

This script is to to be utilized for creating group roles in PostGIS.
This group role is designed to give basic read-only access to users assigned
to this group role.
The user will be prompted in the command prompt.
The user must input the name of the group role to create.
The user must input the number of schemas to revoke read access to.
The user must input the names of the schemas to revoke access to (the user will
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
    groupName = input("Please enter the name of the group role to create: ") # Read-only group name to be created
    print("Groupname: gr_%s" % groupName)

    # Creates read-only group
    cur.execute("""CREATE ROLE gr_%s NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE NOREPLICATION VALID UNTIL 'infinity';""" % (groupName))
    conn.commit()
    print ("Group Role gr_%s created!\n" % groupName)

# Error check
except psycopg2.Error as f:
    print ("Group Role can't be created!")
    #print f
    print (f.pgcode)
    print (f.pgerror)
    print ("Press Enter to exit...")
    input()

try:
    # Grants connection access to the database to the group role
    cur.execute("""GRANT CONNECT ON DATABASE %s TO gr_%s;""" % (dbName, groupName))
    conn.commit()
    print ("Group Role gr_%s granted database access to %s!\n" % (groupName, dbName))

    # Grants read-only access to all schema(s) in the database and future schema(s)
    cur.execute("""
    DO $do$
    DECLARE sch text;
    BEGIN FOR sch IN SELECT nspname FROM pg_namespace
        LOOP
            EXECUTE format('GRANT USAGE ON SCHEMA %s TO gr_""" + groupName + """', sch);
            EXECUTE format('GRANT SELECT ON ALL TABLES IN SCHEMA %s TO gr_""" + groupName + """', sch);
            EXECUTE format('GRANT SELECT ON ALL SEQUENCES IN SCHEMA %s TO gr_""" + groupName + """', sch);
            EXECUTE format('ALTER DEFAULT PRIVILEGES IN SCHEMA %s GRANT SELECT ON TABLES TO gr_""" + groupName + """', sch);
            EXECUTE format('ALTER DEFAULT PRIVILEGES IN SCHEMA %s GRANT SELECT ON SEQUENCES TO gr_""" + groupName + """', sch);
        END LOOP;
    END;
    $do$
    LANGUAGE plpgsql;""")
    conn.commit()
    print ("Group Role gr_%s granted schema and table read only.\n" % groupName)

    # Revokes all access to a specific schema
    numbRevoke = int(input("Please enter the number of schemas to revoke read access for this group policy: "))

    # Loop for revoking schema access
    counter = 0
    while numbRevoke > counter:
        schemaExcept = input ("Please enter the name of the schema to revoke read access: ")
        cur.execute('REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA %s FROM GROUP gr_%s;' %(schemaExcept, groupName))
        conn.commit()
        print ("Group Role gr_%s not given access to %s.\n" %(groupName, schemaExcept))
        counter += 1

    # Closes database connection
    conn.close()
    print ("Database Connection Closed!\n")
    input("Press Enter to exit...")

# Error check
except psycopg2.Error as f:
    print ("Group Role not granted access!")
    #print f
    print (f.pgcode)
    print (f.pgerror)
    print ("Press Enter to exit...")
    input()
