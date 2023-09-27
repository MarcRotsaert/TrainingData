#!/bin/bash 
composefile=python-mongo-polar.yaml
su_container_file=docker/compose/up.sh

result_compose=$(docker-compose ls)
echo "$result_compose"
linenr_compose=$(awk -v pattern="$composefile" '$0 ~ pattern {print NR}' <<< "$result_compose")
echo "$linenr_compose"
if [[ $linenr_compose ]]
then
    result_status=$(awk 'NR=="'"$linenr_compose"'" {print $2}' <<< "$result_compose") 
    if [[ "$result_status" == 'running(1)' ]]
    then
        echo 'mongo database already started'
    else
        echo 'startup mongo database'
        source "$su_container_file" docker/compose/python-mongo-polar.yaml
    fi 
else
    echo 'startup mongo database'
    source "$su_container_file" docker/compose/python-mongo-polar.yaml
fi 
