#!/bin/bash
env=sandbox
RED='\033[0;31m'
echo "clone latest code from git"
code_dir="`pwd`/<repo>/"
[ -d $code_dir ] && sudo rm -rf $code_dir && echo "Old code directory removed !"
# change this to git clone https://<Personal Access Token>@github.com/<repo>/<repo>.git
echo "cloning branch: $1"
git clone -b $1 git@github.com:<repo>/<repo>.git
echo "copying latest config to code"
cp config.json <repo>/
cd <repo>
echo "setting up docker"
docker rm -f $(docker ps -a | grep 'spark-local' | awk '{ print $1 }')
docker rmi -f $(docker images | grep 'spark-local' | awk '{ print $3 }')
docker image build -t spark-local .
docker run --name spark-local -p 8000:8080 -p 18080:18080 -v /home/deepak/<repo>/:/<repo> -dit spark-local
echo "Running build command inside docker"
docker exec -it spark-local /bin/bash -c "cd <repo> && make build-prod"
echo "Uploading py.zip files to s3"
aws s3 cp dist s3://logsetl-<repo>-emr/py-dist/ --recursive