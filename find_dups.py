#!/usr/bin/python
# GPL V3 licenced
#
# Jon Schlueter <jon.schlueter@gmail.com>
#
# Find duplicates and update the duplicate_list table

import sqlite3

db_filename = 'index_stuff.db'

con = sqlite3.connect(db_filename)

if con:

    con.execute('DELETE from duplicate_list')
    con.execute('INSERT OR IGNORE INTO folder_list (path) SELECT DISTINCT path from file_list')

    cursor = con.execute('SELECT distinct group_concat(path), type from file_list WHERE md5sum in (SELECT md5sum from duplicate_list where count > 1) GROUP BY md5sum')

    for row in cursor:
        print row

    con.commit()
    con.close()

