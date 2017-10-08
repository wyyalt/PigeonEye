#!bin/bash

for i in $(seq 1 30);
do
    echo $i
    pid=`ps -ef |grep $1 |grep -v sshpass |grep -v grep |grep -v session_tracker.sh| awk '{print $2}'`
    if [ ! -z "$pid" ];
    then
        echo "Start Run Strace......"
        sudo strace -fp $pid -t -o ssh_audit_$2.log;
        break;
    fi;
    sleep 1
done;


