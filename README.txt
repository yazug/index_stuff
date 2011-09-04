index_stuff

a cleanup/indexing tool for finding and eliminating duplicate files

Stores path,filename,type,size,last modified,created,md5sum of files it indexes

Work in progress

GPL V3 licenced

Jon Schlueter
jon.schlueter@gmail.com


To Index a set of folders
Run:
    index_stuff.py

To remove folders from the DB which are no longer present in OS
run:
    check_paths.py


Find mp3s without type set
select * from file_list where filename like "%.mp3";

update file_list set type = "mp3" where type is null and filename like "%.mp3";

update file_list set type = "empty" where size = 0;



select distinct path from file_list where type = "mp3";


select type, count(filename) from file_list group by type;

select distinct type from file_list;



update file_list set type = "code" where type is null and filename like "%.c";
update file_list set type = "code" where type is null and filename like "%.cpp";
update file_list set type = "code" where type is null and filename like "%.h";
update file_list set type = "code" where type is null and filename like "%.java";
update file_list set type = "code" where type is null and filename like "%.pl";
update file_list set type = "code" where type is null and filename like "%.py";
update file_list set type = "doc" where type is null and filename like "%.doc";
update file_list set type = "tbz2" where type is null and filename like "%.tar.bz2";
update file_list set type = "tbz2" where type is null and filename like "%.tbz2";
update file_list set type = "tgz" where type is null and filename like "%.tar.gz";
update file_list set type = "tgz" where type is null and filename like "%.tgz";
update file_list set type = "xml" where type is null and filename like "%.xml";
update file_list set type = "video" where type is null and filename like "%.avi";

update file_list set type = "xls" where type is null and filename like "%.xls";
update file_list set type = "zip" where type is null and filename like "%.zip";
update file_list set type = "exe" where type is null and filename like "%.exe";
update file_list set type = "sh" where type is null and filename like "%.sh";
update file_list set type = "ps" where type is null and filename like "%.ps";
update file_list set type = "pdf" where type is null and filename like "%.pdf";
update file_list set type = "txt" where type is null and filename like "%.txt";
update file_list set type = "txt" where type is null and filename like "%.TXT";
update file_list set type = "tml" where type is null and filename like "%.tml";



