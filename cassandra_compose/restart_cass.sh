
#!bin/sh

# A shell script to quickly restart the Cassandra container

CONTAINER_NAME="cassandra0"
NETWORK_NAME="some-net"


docker container stop $CONTAINER_NAME
docker container rm $CONTAINER_NAME
docker-compose up -d
docker network connect $NETWORK_NAME $CONTAINER_NAME
