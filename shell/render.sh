#!/bin/sh

# author: web
# usage:
# render.sh -i template -o filename

global_var=""

##### define zone #####
foo=bar
##### define zone #####

parse_line() {
  local line="$1"
  if [[ "$line" == *"{{ "*" }}"* ]];then
    # get vars in "{{ var }}{{ var1 }}.." 
    # put them in array
    var_array=(`echo "$line"|grep -oP '{{ \w+ }}'|grep -oP '\w+'|awk '{print $1}'`)
    for var in ${var_array[@]}
    do
      replace $var
      line=`echo "$line"|sed "s+{{ $var }}+$global_var+"`
    done
    echo "$line" >> $output
  else
    echo "$line" >> $output
  fi
}

replace() {
  local value="${!1}" # get value of variable that declare in define zone
  if [ ! $value ];then
    global_var="{{ $1 }}"
  else
    # '&' cannot work in sed, so turn '&' into '\&'
    value=`echo ${value/&/\\\\&}`
    global_var="$value"
  fi
}

main() {
  while getopts ":i:o:" opt; do
    case $opt in
      i)
        input=$OPTARG
        ;;
      o)
        output=$OPTARG
        ;;
      \?)
        echo "Invalid option: -$OPTARG" >&2
        ;;
    esac
  done
  
  output_base_dir=`dirname $output`
  if [ ! -d $output_base_dir ];then
    mkdir -p $output_base_dir
  fi
  
  rm -f $output && touch $output
  
  cat $input | while read -r line
  do
    if [[ ${line:0:1} == "#" ]];then
      echo $line >> $output
    else
      parse_line "$line"
    fi
done
}

main()
