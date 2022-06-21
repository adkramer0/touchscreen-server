echo killing old doker processes
docker-compose rm -fs

echo building docker containers
docker-compose up --build -d