
#!bin/sh

# A shell script to quickly rebuild the app

APP_NAME="myapp"
IMAGE_NAME="one"
NETWORK_NAME="some-net"


docker container stop $APP_NAME
docker container rm $APP_NAME
docker build -t $IMAGE_NAME .
docker run --name $APP_NAME -d -p 4000:80 $IMAGE_NAME:latest
docker network connect $NETWORK_NAME $APP_NAME


# docker logs $APP_NAME

# docker exec -it cassandra0 cqlsh
# select * from mykeyspace.ImgCls
