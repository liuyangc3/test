#!/bin/sh

# author web
# usage: build.sh <project name>


projectName=$1
jenkinsHost=172.16.200.111:8090
jenkinsUser=dbn_admin
jenkinsPasswd='dbn#@#002385'

urlPrefix=http://$jenkin/job/$projectName

# functions
getBuildId() {
    echo `curl -s $urlPrefix/lastBuild/api/json?tree=id | grep -oP "\d+"`
}

isBuilding() {
    echo `curl -s $urlPrefix/$currentBuildId/api/json?tree=building | grep -oP "(?<={\"building\":)\w+"`
}

# get last build id
lastBuildId=`getBuildId`
currentBuildId=$[lastBuildId+1]

# do job build

curl --user $jenkinsUser:$jenkinsPasswd -XPOST -s $urlPrefix/build

while [ "`getBuildId`" != "$currentBuildId" ]
do
  sleep 3
  echo $projectName $currentBuildId not start yet
done


# check wether the current build task is building

while [ "`isBuilding`" = "true" ]
do
    echo $projectName $currentBuildId is building...
    sleep 3
done


result=`curl -s $urlPrefix/$currentBuildId/api/json?tree=result | grep -oP "(?<={\"result\":\")\w+"`

if [ "$result" =  "SUCCESS" ];then
   echo "$projectName $currentBuildId 构建成功"
fi

if [ "$result" =  "FAILURE" ];then
   echo "$projectName $currentBuildId 构建失败"
fi
