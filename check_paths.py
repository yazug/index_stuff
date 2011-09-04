#!/usr/bin/python
# GPL V3 Licenced
#
# Jon Schlueter <jon.schlueter@gmail.com>
#

import sqlite3
import sys,os

con = sqlite3.connect('index_stuff.db')

cursor = con.execute('SELECT distinct path from file_list where type = "mp3"')

for (path) in cursor:
    if not os.path.isdir(path[0]):
        print "[%s] is missing removing entries"%path[0]
        con.execute( 'delete from file_list where path = "'+path[0]+'"')
        con.commit()

