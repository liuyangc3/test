#!/bin/sh

DATABASES_TO_EXCLUDE="cas esp hive oozie"   # 需要排除的数据库
BACKUP_PATH=/data0/backup
date=`date +%F

gen_SQLSTMT(){
  local exclude_databases
  local system_db="'mysql','test','information_schema','performance_schema'"  # 排除系统库
  for db in `echo $DATABASES_TO_EXCLUDE`; do
    exclude_databases="$system_db,'$db'"
  done
  SQLSTMT="SELECT schema_name FROM information_schema.schemata WHERE schema_name NOT IN ($exclude_databases);"
}

do_mysqldump(){
  mkdir -p $BACKUP_PATH/$date
  for db in `mysql -ANe"${SQLSTMT}"`; do
    mysqldump -uroot -p --set-gtid-purged=OFF --default-character-set=utf8 $db > $BACKUP_PATH/$date/$db.sql
  done
}

do_xbackup(){
  innobackupex --user=root --password='' $BACKUP_PATH/$date/ --no-timestamp
  innobackupex --apply-log $BACKUP_PATH/$date/
}
