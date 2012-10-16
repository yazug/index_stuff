#!/usr/bin/python
# GPL V3 Licenced
#
# Jon Schlueter <jon.schlueter@gmail.com>
#
# Look through the database and remove deleted directories

import os
import sqlite3
import sys

db_filename = 'index_stuff.db'

con = sqlite3.connect(db_filename)

delete_limit = 10
if con:

    con.execute('INSERT OR IGNORE INTO folder_list (path) SELECT DISTINCT path from file_list')
    cursor = con.execute('SELECT path,foldername FROM folder_list')

    for (path, foldername) in cursor:
        if not os.path.isdir(path) and delete_limit > 0:
            print "[%s] is missing removing entries"%(path.encode('utf-8'),)
            con.execute( 'delete from file_list where path = "'+path.encode('utf-8')+'"')
            con.execute( 'delete from folder_list where path = "'+path.encode('utf-8')+'"')
            con.commit()
            delete_limit = delete_limit - 1

        if not os.path.basename(path) == foldername:
            print "Mismatch of path and foldername [%s] [%s]"%(path, foldername,)
            con.execute( 'delete from file_list where path = "'+path.encode('utf-8')+'"')
            con.execute( 'delete from folder_list where path = "'+path.encode('utf-8')+'"')
            con.commit()
            delete_limit = delete_limit - 1

        if delete_limit == 0:
            break;

    con.close()

