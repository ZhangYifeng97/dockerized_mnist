
#!bin/sh

# A shell script to quickly rebuild the app








docker container stop myapp
docker container rm myapp
docker build -t one .
docker run --name myapp -d -p 4000:80 one:latest
docker network connect some-net myapp


# select * from mykeyspace.ImgCls
