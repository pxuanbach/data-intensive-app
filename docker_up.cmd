docker network create -d bridge kafka-network
docker-compose -f ./kafka/docker-compose.yml up -d
docker-compose -f ./deligator_group/docker-compose.yml up -d
docker-compose -f ./downloader_group/docker-compose.yml up -d
docker-compose -f ./detection_group/docker-compose.yml up -d