#!/usr/bin/python
# GPL V3 licence
# Jon Schlueter <jon.schlueter@gmail.com>
# This script will create an empty DB which can be used by the index_stuff.py script

import sqlite3


con = sqlite3.connect("index_stuff.db")

sql = "CREATE TABLE if not exists file_list (path TEXT, filename TEXT, type TEXT, size NUMERIC, mdate INTEGER, cdate INTEGER, md5sum TEXT);"

con.execute(sql)


con.execute("create index if not exists index_file_list_type on file_list (type);")
con.execute("create index if not exists index_file_list_path on file_list (path);")
con execute("CREATE TABLE folder_list(path TEXT, foldername TEXT, folder_count integer, file_count integer, mdate INTEGER, cdate INTEGER, last_checked DATE);")



con.commit();

con.close();
