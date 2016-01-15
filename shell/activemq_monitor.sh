#!/bin/bash

# check activemq internal status
# author liuyangc33@gmail.com
usage() {
    cat << EOF
`basename $0`: [option]
    -c --connection        Show client ip which connected.
    -t --topic topname     Show topic information
                           VirtualTopic only need pass "name" in VirtualTopic.name.topic
    -q --queue queueuname  Show quque information 
EOF
}

# set activemq install path
readonly ACTIVE_HOME=/opt/apache-activemq-5.11.1
readonly ACTIVE_CONF=$ACTIVE_HOME/conf/activemq.xml

filter() {
  local stdin
  while read line; do
  # filter information
  echo "$line" | awk '/EnqueueCount/{
            gsub(/ /,"",$0);
            # pass into shell function
            printf("local %s\n", $0);
        }
        /DispatchCount/{
            gsub(/ /,"",$0);
            printf("local %s\n", $0); 
        }
        /Subscriptions/{
            # $0 format: Subscriptions = [org.apache.activemq:xxx, org.apache.activemq:xx2, ...]
            len=length($0); 
            split(substr($0,18,len-18), Subscribers," ");
    
            printf("local clientIdArray=(");  # pass into shell function
            for(i in Subscribers){
                # format:  org.apache.activemq:type=Broker,...clientId=<clientid>,consumerId=xxxx..
                line = Subscribers[i];
                # awk regx is ERE, dont support lookhead
                match(line, /clientId=(.+),consumerId/);
                # 9:clientId=  10:consumerId  20:clientId=,consumerId
                clientId = substr(line,RSTART+9,RLENGTH-20);
                printf("%s ", clientId);
            }
            printf(")\n") # close var clientIdArray
        }
        /DequeueCount/{
            gsub(/ /,"",$0);
            printf("local %s\n", $0);
        }'
  done

  # awk output will like this:
  # local EnqueueCount=110
  # local clientIdArray=(ID_PC1-51403-635856995754326450-2_0 ID_PC2-50409-635856801075547118-2_0)
  # local DispatchCount=332
  # local DequeueCount=330
}

getTopicStatus() {
    local topicName="$1"
    $ACTIVE_HOME/bin/activemq-admin query --objname type=Broker,brokerName=$brokerName,destinationType=Topic,destinationName=$topicName|filter
}

getQueueStatus() {
    local queueName="$1"
    $ACTIVE_HOME/bin/activemq-admin query --objname type=Broker,brokerName=$brokerName,destinationType=Queue,destinationName=$queueName| filter
}

format() {
    # useage: format callback cb_args
    local line
    local key
    local callback="$1"
    declare -a keys
    shift

    while read -r line; do
        eval $line  # pass awk var into shell
        key=`echo $line | sed -e 's/=.*$//'`
        key=${key#*local }  # delete local
        keys+=($key)
    done <<< "`$callback $@`"
    
    echo clients:
    for clientId in ${clientIdArray[@]}; do
        echo -e "\t$clientId"
    done
    echo

    unset clientIdArray

    for key in ${keys[@]}; do
        if [[ "$key" == "clientIdArray" ]]; then
            continue
        fi
        echo -e "$key:\t${!key}"
    done
}

showTopicStatus() {
    local topic=VirtualTopic.$1.topic
    echo
    echo $topic
    echo ------------------------------------
    format "getTopicStatus" "$topic"
}

showQueueStatus() {
    local queue="$1"
    echo
    echo $queue
    echo ------------------------------------
    format "getQueueStatus" "$queue"
}

showRemote() {
    $ACTIVE_HOME/bin/activemq-admin query --objname type=Broker,brokerName=$brokerName,connector=clientConnectors,connectorName=openwire,connectionViewType=remoteAddress,connectionName=*|
    sed -n '/Connecting to pid:/,${//!p}'|
    awk 'BEGIN{FS="\n";RS="";printf("Remote Adderss\t\tConnected\n")}
    {
        if(substr($6,0,9) == "Producers") {
            printf("%s\t%s\n", substr($7,23),substr($10,13))
        } else {
            printf("%s\t%s\n", substr($6,23),substr($9,13))
        }    
    }'
}


# get brokername
readonly brokerName=$(grep -oP '(?<=<broker xmlns="http://activemq.apache.org/schema/core" brokerName=")\w+' $ACTIVE_CONF)
readonly ARGS=`getopt -n "$PROG" -a -o t:q:ch -l topic:,queue:,connection,help -- "$@"`
[ $? -ne 0 ] && usage 1
eval set -- "${ARGS}"

while true; do
    case "$1" in
    -t|--topic)
        showTopicStatus $2
        shift 2
        ;;
    -q|--queue)
        showQueueStatus $2
        shift 2
        ;;
    -c|--connection)
        showRemote
        break
        ;;
    -h|--help)
        usage
        ;;
    --)
        shift
        break
        ;;
    esac
done
