docker-compose stop $1
docker-compose rm -f $1
docker-compose up --force-recreate -d $1
