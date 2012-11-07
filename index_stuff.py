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

db_filename = 'index_stuff.db'

con = sqlite3.connect(db_filename)

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

extention_type_list = [
        ('.avi','video'),
        ('.c','code'),
        ('.cpp','code'),
        ('.css','css'),
        ('.dll','dll'),
        ('.doc','doc'),
        ('.docx','docx'),
        ('.exe','exe'),
        ('.gif','gif'),
        ('.h','code'),
        ('.htm','html'),
        ('.html','html'),
        ('.java','code'),
        ('.jpg','jpg'),
        ('.JPG','jpg'),
        ('.js','js'),
        ('.mp3','mp3'),
        ('.m4a','music'),
        ('.pdf','pdf'),
        ('.pl','code'),
        ('.png','png'),
        ('.png.gz','png'),
        ('.ps','ps'),
        ('.py','code'),
        ('.sh','sh'),
        ('.tar.bz2','tbz2'),
        ('.tar.gz','tgz'),
        ('.tbz2','tbz2'),
        ('.tgz','tgz'),
        ('.tif','tif'),
        ('.tiff','tif'),
        ('.txt','txt'),
        ('.xls','xls'),
        ('.xml','xml'),
        ('.zip','zip'),
        ('.o','build_object'),
        ('.lo','build_object'),
        ('.a','build_object'),
        ('.la','build_object'),
        ('.lib','library'),
        ('Makefile','makefile'),
        ('SConscript','makefile'),
        ('SConstruct','makefile'),
        ('.db','database'),
        ]

def index_file(path,name,con):
    filename = os.path.join(path,name)

    if os.path.isfile(filename) :
        size = os.path.getsize(filename)
        last_modified = os.path.getmtime(filename)
        created = os.path.getctime(filename)
        file_type = ""
        if size == 0:
            file_type = "empty"
        else:
            for exten, exten_type in extention_type_list:
                if exten in name:
                    file_type = exten_type

        md5sum = md5file(filename)

        sql = ("insert or replace into file_list (path,filename,md5sum,size,mdate,cdate,type) values " +
            "(\"%s\", \"%s\", '%s', %d, %d, %d, '%s')")%(path, name, md5sum,size,last_modified,created,file_type)

        try:
            con.execute(sql)
            con.commit()
        except:
            print "Failed on the following:"
            print (path, name, md5sum, size, last_modified, created)
            print sql

def walkfunc(arg, dirname, names):
    check_again = True

    #print "Walk here ",arg,dirname,names

    sql_find = ("select * from file_list where path = \"%s\"")%(dirname.encode('utf-8'))
    check_again = False

    dir_count = 0
    file_count = 0

    for name in names:
        filename = os.path.join(dirname.encode('utf-8'),name.encode('utf-8')).encode('utf-8')
        if os.path.isfile(filename):
            file_count += 1

        if os.path.isdir(filename):
            dir_count += 1

    print "Got %d folders and %d files"%(dir_count,file_count)
    cursor = arg.execute('select path,folder_count,file_count from folder_list where path = \"%s\"'%(dirname.encode('utf-8'),))
    check_again = True
    for row in cursor:
        print row
        print "Folder Record [%s] has %s folders and %s files"%(row[0], row[1], row[2])
        if row[1] is None:
            check_again = True
        elif row[2] is None:
            check_again = True
        elif row[2] != file_count and row[1] != folder_count:
            check_again = True
        else:
            check_again = False

    try:
        con = arg.execute(sql_find)

        db_list = con.fetchall()

        name_list = []
        for record in db_list:
            path = record[0]
            name = record[1]
            filename = os.path.join(dirname.encode('utf-8'),name.encode('utf-8'))

            if os.path.isfile(filename):
                if name.encode('utf-8') not in names:
                    check_again = True;
                    print "File not there anymore [%s]"%name.encode('utf-8')

                name_list.append(name.encode('utf-8'))
            else:
                print "Folder here.... [%s]"%name.encode('utf-8')


        if len(db_list) == len(name_list):
            pass
        else:
            check_again = True

        if check_again:
            print "Reindex needed for [%s]"%(dirname)
            print "Got [db:%d] vs [fs:%d] records"%(len(db_list),len(name_list))
        else:
            print "Same Nothing to do [%s]"%(dirname.encode('utf-8'),)

    except Exception as inst:
        print "Failed on the following exception [%s]:"%(inst)
        print sql_find



    if check_again:
        sql = "delete from file_list where path = \"%s\""%dirname.encode('utf-8')
        try:
            arg.execute(sql)
        except:
            print "Failed to try to cleanup [%s] with sql [%s]"%(dirname.encode('utf-8'),sql)

        for file in names:
            index_file(dirname.encode('utf-8'),file.encode('utf-8'),arg)

        sql = "INSERT OR REPLACE INTO folder_list (path, foldername, folder_count, file_count, cdate,mdate,last_checked) values ('%s','%s',%d, %s, %s,%s,%s)"
        params = (dirname.encode('utf-8'), os.path.basename(dirname).encode('utf-8'),dir_count,file_count,os.path.getctime(dirname),os.path.getmtime(dirname),'2012-10-15',)
        print sql%params
        arg.execute(sql%params)
        arg.commit()


    print ""

def walkfunc_folders_only(arg, dirname, names):
    folder_list = []
    file_list = []
    for name in names:
        filename = os.path.join(dirname,name)
        if os.path.isdir(filename):
            folder_list.append(name)
        if os.path.isfile(filename):
            file_list.append(name)

    sql_dir_limit = "select * from folder_list where path='%s'"%(dirname.encode('utf-8'))
    #print "Directory Limiting sql[%s]"%sql_dir_limit
    #print folder_list
    print "Walk [%s]"%dirname

    folder_count = len(folder_list)
    file_count = len(file_list)

    last_modified = os.path.getmtime(dirname)
    created = os.path.getctime(dirname)

    path,name = os.path.split(dirname)
    #print "(path, name, Folder Count, file count, cdate, mdate)"
    #print "(\"%s\",\"%s\",%d,%d,%d,%d)"%(path.encode('utf-8'),name.encode('utf-8'),folder_count,file_count,0,0)

    #sql = "insert or replace into folder_list (path,foldername,folder_count,file_count,cdate,mdate) values (\"%s\",\"%s\",%d,%d,%d,%d)"%(path.encode('utf-8'),name.encode('utf-8'),folder_count,file_count,last_modified,created)


    walkfunc(arg,dirname,names);
    print "Testing [%s]" % (sql,)
    #arg.execute(sql)
    #arg.commit()

if True:
    #os.path.walk("/media/DROBO/AudioBooks",walkfunc_folders_only,con)
    #os.path.walk("/media/DROBO/jon_music_2",walkfunc_folders_only,con)
    #os.path.walk("/media/DROBO/jon_music",walkfunc_folders_only,con)
    #os.path.walk("/media/DROBO/stuff",walkfunc_folders_only,con)
    #os.path.walk("/media/DROBO/incoming/eBooks",walkfunc_folders_only,con)
    #os.path.walk("/media/DROBO/corinne-backups",walkfunc_folders_only,con)
    #os.path.walk("/media/DROBO/music",walkfunc_folders_only,con)
    #os.path.walk("/media/DROBO/podcasts",walkfunc_folders_only,con)
    #os.path.walk("/media/DROBO/personal",walkfunc_folders_only,con)
    #os.path.walk("/media/DROBO/other",walkfunc_folders_only,con)
    #os.path.walk("/media/DROBO/reef-stuff",walkfunc_folders_only,con)
    #os.path.walk("/media/DROBO/games",walkfunc_folders_only,con)
    #os.path.walk("/media/DROBO/backup-thumb",walkfunc_folders_only,con)
    #os.path.walk("/media/DROBO/carputer",walkfunc_folders_only,con)
    #os.path.walk("/media/DROBO/all_pictures",walkfunc_folders_only,con)
    #os.path.walk("/media/DROBO/7-13-08",walkfunc_folders_only,con)
    #os.path.walk("/media/DROBO/backup-tools",walkfunc_folders_only,con)
    #os.path.walk("/media/DROBO/ebook",walkfunc_folders_only,con)
    #os.path.walk("/media/DROBO/ebooks",walkfunc_folders_only,con)
    #os.path.walk("/media/DROBO/iso",walkfunc_folders_only,con)
    #os.path.walk("/media/DROBO/install",walkfunc_folders_only,con)
    #os.path.walk("/media/DROBO/linux-laptop-archive",walkfunc_folders_only,con)
    os.path.walk("/media/DROBO",walkfunc_folders_only,con)

if False:
    #os.path.walk("/media/DROBO/stuff",walkfunc,con)
    #os.path.walk("/media/DROBO/jon_music",walkfunc,con)
    #os.path.walk("/media/DROBO/jon_music_2",walkfunc,con)
    os.path.walk("/media/DROBO/AudioBooks",walkfunc,con)
    #os.path.walk("/media/DROBO/incoming/Music",walkfunc,con)
    #os.path.walk("/media/DROBO/incoming/EveOnline",walkfunc,con)
    #os.path.walk("/media/DROBO/incoming/downloads",walkfunc,con)
    #os.path.walk("/media/DROBO/incoming/Dropbox",walkfunc,con)
    #os.path.walk("/media/DROBO/incoming/eBooks",walkfunc,con)
    #os.path.walk("/media/DROBO/linux-laptop-archive",walkfunc,con)
    #os.path.walk("/media/DROBO/linux-laptop-archive/",walkfunc,con)
    #os.path.walk("/media/DROBO/quark_backup_20100121/jon_music/",walkfunc,con)
    #os.path.walk("/media/DROBO/quark_backup_20100121/music",walkfunc,con)
    #os.path.walk("/media/DROBO/music",walkfunc,con)
    #os.path.walk("/media/DROBO/incoming/deadmau5",walkfunc,con)
    #os.path.walk("/media/DROBO/incoming/thumb-dumps/8gb_drive/music",walkfunc,con)
    #os.path.walk("/media/DROBO/incoming/yazug-black/jon_music/misc2",walkfunc,con)
    #os.path.walk("",walkfunc,con)
    #os.path.walk("/media/DROBO/quark",walkfunc,con)
    #os.path.walk("/media/DROBO/quark_backup_20100121",walkfunc,con)

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


if False:
    print "updating types"
    con.execute('update file_list set type = "empty" where size = 0 and type is null')
    con.commit()

if False:
    for exten, exten_type in extention_type_list:
        count_cursor = con.execute('select count(filename) from file_list where type = "'+exten_type+'"')
        before_count = count_cursor.fetchall()[0]

        print 'update file_list set type = "'+exten_type+'" where type is null and filename like "%'+exten+'"'
        con.execute('update file_list set type = "'+exten_type+'" where type is null and filename like "%.'+exten+'"')
        con.commit()
        count_cursor = con.execute('select count(filename) from file_list where type = "'+exten_type+'"')
        count = count_cursor.fetchall()[0]
        print "finished updating %s to %s for a total of %s from %s"%(exten,exten_type,count[0],before_count[0])

    print "Finished updating types"

con.close()
