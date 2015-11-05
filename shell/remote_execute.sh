#!/bin/sh
# usage:
# ./remote_execute.sh 192.168.1.1 'passwd' hostname

ip=$1
passwd=$2
passwd=`echo ${passwd/$/\\\\$}`  # $ --> \$
passwd=`echo ${passwd/&/\\&}`    # & --> \&

auto_ssh_copy() {
  # copy id_rsa.pub to remote
  local ip=$1
  local passwd=$2

expect << EOF
set timeout -1
# exp_internal 1 for debug
spawn sudo -u jenkins ssh-copy-id root@$ip
expect { 
  "*yes/no" {
    send "yes\r"
    exp_continue
  }
  "*password:" {
    puts "\n开始发送密码..."
    send "$passwd\r"
    exp_continue
  }
  eof {
    send_user "eof\n"
    exit
  }
  timeout {
    send \003
    send_user "timeout \n"
    exit
  }
}
EOF
}

remote_execute() {
  # execute command on remote
  # and save command output in a shell variable
  local command="$1"
  local output=$(
  expect << EOF
set timeout -1
#exp_internal 1
log_user 0
spawn ssh root@$ip
expect "*~]#" {
  send "$command\r"
}
expect "$command" {}   
expect -re {\n(.*)\n.*} {
  set hostname \$expect_out(1,string)
}
send "exit\r"
puts \$hostname
close
exit
EOF
)
  echo $output
}

# main
auto_ssh_copy_id $ip $passwd
remote_execute $3
