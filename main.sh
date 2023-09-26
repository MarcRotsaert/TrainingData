
composefile=python-mongo-polar.yaml
# composefile="python"
# docker-compose ls > 'test.txt'
result_compose=`docker-compose ls`
echo $result_compose
linenr_compose=`awk '/'"$composefile"'/ {print NR}' <<< "$result_compose"`
echo $linenr_compose
if [[ $linenr_compose ]]
then
    if [[ "$result_status"=='running(1)' ]]
    then
        echo 'mongo database already started'
    else
        source docker/compose/up.sh docker/compose/python-mongo-polar.yaml
    fi 
else
    echo 'startup mongo database'
    source docker/compose/up.sh docker/compose/python-mongo-polar.yaml
fi 
