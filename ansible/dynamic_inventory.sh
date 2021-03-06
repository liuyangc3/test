#!/bin/sh
# shell version for ansible dynamic inventory hosts

gen_inventorys_json() {
  local inventory_group=tomcat
  local network_prefix=192.168.0
  printf "{\"$inventory_group\": ["
  for i in {1..254}; do
    printf "\"$network_prefix.%s\"," $i
  done
  printf "\"$network_prefix.255\"]}"
}

inventorys=`gen_inventorys_json`

get_host_info() {
  local host=$1
  echo '{'$host':{"ansible_ssh_host": "'$host'", "ansible_ssh_port": 22, "ansible_ssh_user": "root"}}'
}


# support --host=192.168.1.1 and --list

while getopts "h-:" arg; do
  case $arg in
    -) # match dubble --
      host_ip="${OPTARG#*=}"  # string after '='
        case $OPTARG in
          host=?*)
            get_host_info "$host_ip"
            ;;
          list)
            echo $inventorys
            ;;
          '')  # "--" will terminate
            break
            ;;
          *)
            echo "Illegal option --$OPTARG" >&2
            exit 2
            ;;
        esac
      ;;
    h)
      echo
      echo -e "--host=host\t\t\t返回指定host信息"
      echo -e "--list\t\t\t\t返回所有host信息"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done
