Skip to content
 

Search…
All gists
GitHub
New gist
@liuyangc3
 Edit
  Delete
  Star 0
  @liuyangc3liuyangc3/show_mysql_performance.sh
Last active a month ago
Embed  
<script src="https://gist.github.com/liuyangc3/5c68453bde44c5374b8f.js"></script>
  Download ZIP
 Code  Revisions 2
Raw  show_mysql_performance.sh
#!/bin/sh

usage() {
  cat <<EOF
  `basename $0` prot [interval]
  prot      MySQL 实例端口
  interval  输出间隔时间,默认1s 
EOF
  exit 1
}

if test -n "$@"; then
  usage
fi

# 参数为空时 默认使用1秒 
pertime=$2
if [ $pertime -ne ];then
    pertime=1
fi

# 使用 mysqladmin 监控性能

prog=/usr/local/mysql/bin/mysqladmin
export MYSQL_PWD='ZI@U#Ay=**'
$prog -uroot -S /tmp/mysql_$1.sock -r -i $pertime extended-status |\
awk -F"|" \
"BEGIN{ count=0; }"\
'{ if($2 ~ /Variable_name/ && ++count == 1){\
    print "----------|---------|--- MySQL Command Status --|----- Innodb row operation ----|-- Buffer Pool Read --";\
    print "---Time---|---QPS---|select insert update delete|  read inserted updated deleted|   logical    physical";\
}\
else if ($2 ~ /Queries/){queries=$3;}\
else if ($2 ~ /Com_select /){com_select=$3;}\
else if ($2 ~ /Com_insert /){com_insert=$3;}\
else if ($2 ~ /Com_update /){com_update=$3;}\
else if ($2 ~ /Com_delete /){com_delete=$3;}\
else if ($2 ~ /Innodb_rows_read/){innodb_rows_read=$3;}\
else if ($2 ~ /Innodb_rows_deleted/){innodb_rows_deleted=$3;}\
else if ($2 ~ /Innodb_rows_inserted/){innodb_rows_inserted=$3;}\
else if ($2 ~ /Innodb_rows_updated/){innodb_rows_updated=$3;}\
else if ($2 ~ /Innodb_buffer_pool_read_requests/){innodb_lor=$3;}\
else if ($2 ~ /Innodb_buffer_pool_reads/){innodb_phr=$3;}\
else if ($2 ~ /Uptime / && count >= 2){\
  printf(" %s |%9d",strftime("%H:%M:%S"),queries);\
  printf("|%6d %6d %6d %6d",com_select,com_insert,com_update,com_delete);\
  printf("|%6d %8d %7d %7d",innodb_rows_read,innodb_rows_inserted,innodb_rows_updated,innodb_rows_deleted);\
  printf("|%10d %11d\n",innodb_lor,innodb_phr);\
}}'
 @liuyangc3
 Styling with Markdown is supported
Write Preview

Leave a comment
Attach files by dragging & dropping,  选择文件 selecting them, or pasting from the clipboard.
Comment
Status API Training Shop Blog About Pricing
© 2016 GitHub, Inc. Terms Privacy Security Contact Help
