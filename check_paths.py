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

    cursor = con.execute('SELECT DISTINCT path FROM file_list WHERE type IS NOT NULL AND type <> "empty"')

    for (path) in cursor:
        if not os.path.isdir(path[0]) and delete_limit > 0:
            print "[%s] is missing removing entries"%path[0]
            con.execute( 'delete from file_list where path = "'+path[0]+'"')
            con.commit()
            delete_limit = delete_limit - 1

    con.close()

