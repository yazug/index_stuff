#!/usr/bin/python
# GPL V3 licenced
#
# Jon Schlueter <jon.schlueter@gmail.com>
#
# This script is a work in progress.  currently it indexes the specified
# paths and puts information into the DB
#
# Supports looking for the folder in the DB and if no files have been
# added/removed it won't reindex the folder

import sys,os
import sqlite3
import hashlib

con = sqlite3.connect("index_stuff.db")


def md5file(filename):
    """Return the hex digest of a file without loading it all into memory"""
    fh = open(filename)
    digest = hashlib.md5()
    while 1:
        buf = fh.read(4096)
        if buf == "":
            break
        digest.update(buf)
    fh.close()
    return digest.hexdigest()

def walkfunc(arg, dirname, names):
    check_again = True

    print "Walk here ",arg,dirname,names

    sql_find = ("select * from file_list where path = \"%s\"")%(dirname)
    check_again = False

    try:
        con = arg.execute(sql_find)

        db_list = con.fetchall()

        name_list = []
        for record in db_list:
            path = record[0]
            name = record[1]
            filename = os.path.join(dirname,name)
            if os.path.isfile(filename):
                if name not in names:
                    check_again = True;
                    print "File not there anymore [%s]"%name

                name_list.append(name)
            else:
                print "Folder here.... [%s]"%name


        if len(db_list) == len(name_list):
            pass
        else:
            check_again = True;

        if check_again:
            print "Reindex needed for [%s]"%(dirname)
            print "Got [db:%d] vs [fs:%d] records"%(len(db_list),len(name_list))
        else:
            print "Same Nothing to do [%s]"%(dirname)

    except:
        print "Failed on the following:"
        print sql_find



    if check_again:
        sql = "delete from file_list where path = \"%s\""%dirname
        try:
            arg.execute(sql)
        except:
            print "Failed to try to cleanup [%s] with sql [%s]"%(dirname,sql)

        for file in names:
            filename = os.path.join(dirname,file)
            if os.path.isfile(filename) :
                size = os.path.getsize(filename)
                last_modified = os.path.getmtime(filename)
                created = os.path.getctime(filename)

                md5sum = md5file(filename)

                sql = ("insert into file_list (path,filename,md5sum,size,mdate,cdate) values " +
                    "(\"%s\", \"%s\", '%s', %d, %d, %d)")%(dirname, file, md5sum,size,last_modified,created)
                #print sql
                try:
                    arg.execute(sql)
                except:
                    print "Failed on the following:"
                    print (dirname, file, md5sum, size, last_modified, created)
                    print sql


        arg.commit()

    print ""

if True:
    os.path.walk("/media/DROBO/stuff",walkfunc,con)
    os.path.walk("/media/DROBO/jon_music",walkfunc,con)
    os.path.walk("/media/DROBO/jon_music_2",walkfunc,con)
    os.path.walk("/media/DROBO/linux-laptop-archive",walkfunc,con)
    os.path.walk("/media/DROBO/quark",walkfunc,con)
    os.path.walk("/media/DROBO/quark_backup_20100121",walkfunc,con)

if False:
    #os.path.walk("/media/DROBO/music",walkfunc,con)
    #os.path.walk("/media/DROBO/personal",walkfunc,con)

    #os.path.walk("/media/DROBO/incoming",walkfunc,con)
    os.path.walk("/media/DROBO/backup",walkfunc,con)

    os.path.walk("/media/DROBO/nog-backup",walkfunc,con)
    os.path.walk("/media/DROBO/5f24179b791e54f13475863cbcd237a3",walkfunc,con)
    os.path.walk("/media/DROBO/misc",walkfunc,con)
    os.path.walk("/media/DROBO/mom&dad",walkfunc,con)
    os.path.walk("/media/DROBO/Music",walkfunc,con)
    os.path.walk("/media/DROBO/jon_music",walkfunc,con)
    os.path.walk("/media/DROBO/jon_music_2",walkfunc,con)
    os.path.walk("/media/DROBO/laptop_2009_12",walkfunc,con)
    os.path.walk("/media/DROBO/laptop-archive",walkfunc,con)
    os.path.walk("/media/DROBO/laptop_backup",walkfunc,con)
    os.path.walk("/media/DROBO/Laptop-backup-2009-12",walkfunc,con)
    os.path.walk("/media/DROBO/laptop_stuff",walkfunc,con)
    os.path.walk("/media/DROBO/led_firefly_stuff",walkfunc,con)
    os.path.walk("/media/DROBO/linux_driver_stuff",walkfunc,con)
    os.path.walk("/media/DROBO/linux-laptop-archive",walkfunc,con)
    os.path.walk("/media/DROBO/linux_work",walkfunc,con)
    os.path.walk("/media/DROBO/NavigationSolutions",walkfunc,con)
    os.path.walk("/media/DROBO/quark",walkfunc,con)
    os.path.walk("/media/DROBO/quark_backup_20100121",walkfunc,con)
    os.path.walk("/media/DROBO/podcasts",walkfunc,con)
    os.path.walk("/media/DROBO/podiobooks",walkfunc,con)
    os.path.walk("/media/DROBO/AudioBooks",walkfunc,con)
    os.path.walk("/media/DROBO/backup",walkfunc,con)
    os.path.walk("/media/DROBO/carputer",walkfunc,con)
    os.path.walk("/media/DROBO/ebook",walkfunc,con)
    os.path.walk("/media/DROBO/ebooks",walkfunc,con)
    os.path.walk("/media/DROBO/c_drive",walkfunc,con)
    os.path.walk("/media/DROBO/extern-backup-iris",walkfunc,con)
    os.path.walk("/media/DROBO/game_iso",walkfunc,con)
    os.path.walk("/media/DROBO/games",walkfunc,con)
    os.path.walk("/media/DROBO/install",walkfunc,con)
    os.path.walk("/media/DROBO/iso",walkfunc,con)
    os.path.walk("/media/DROBO/iTunes",walkfunc,con)
    os.path.walk("/media/DROBO/java",walkfunc,con)
    os.path.walk("/media/DROBO/other_corinne",walkfunc,con)
    os.path.walk("/media/DROBO/My\ Received\ Podcasts",walkfunc,con)
    os.path.walk("/media/DROBO/send",walkfunc,con)
    os.path.walk("/media/DROBO/thumb-backup",walkfunc,con)
    os.path.walk("/media/DROBO/thumb_drive_dump",walkfunc,con)
    os.path.walk("/media/DROBO/Trip-Feb-2009",walkfunc,con)
    os.path.walk("/media/DROBO/TSR",walkfunc,con)
    os.path.walk("/media/DROBO/vplogs",walkfunc,con)
    os.path.walk("/media/DROBO/yahoo_briefcase",walkfunc,con)
    os.path.walk("/media/DROBO/zip_disks",walkfunc,con)



con.close()
