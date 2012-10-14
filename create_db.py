#!/usr/bin/python
# GPL V3 licence
# Jon Schlueter <jon.schlueter@gmail.com>
# This script will create an empty DB which can be used by the index_stuff.py

import sqlite3

db_filename = 'index_stuff.db'

con = sqlite3.connect(db_filename)

if con:
    print "Created [%s] db to hold things" % (db_filename,)

    con.execute('CREATE TABLE IF NOT EXISTS file_list (path TEXT, filename TEXT, type TEXT, size NUMERIC, mdate INTEGER, cdate INTEGER, md5sum TEXT)')
    con.execute('CREATE INDEX IF NOT EXISTS index_file_list_type on file_list (type)')
    con.execute('CREATE INDEX IF NOT EXISTS index_file_list_path on file_list (path)')
    con.execute('CREATE INDEX IF NOT EXISTS index_file_list_md5sum on file_list (md5sum)')
    con.execute('CREATE TABLE IF NOT EXISTS folder_list(path TEXT, foldername TEXT, folder_count integer, file_count integer, mdate INTEGER, cdate INTEGER, last_checked DATE)')

    con.execute('CREATE TABLE IF NOT EXISTS duplicate_list (md5sum TEXT, type TEXT, size NUMERIC, count NUMERIC)')

    con.commit()
    con.close()


else:
    print "Failed to open DB Connection to [%s]" % (db_filename,)
