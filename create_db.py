#!/usr/bin/python
# GPL V3 licence
# Jon Schlueter <jon.schlueter@gmail.com>
# This script will create an empty DB which can be used by the index_stuff.py script

import sqlite3


con = sqlite3.connect("index_stuff.db")

sql = "CREATE TABLE file_list (path TEXT, filename TEXT, type TEXT, size NUMERIC, mdate INTEGER, cdate INTEGER, md5sum TEXT);"

con.execute(sql)
