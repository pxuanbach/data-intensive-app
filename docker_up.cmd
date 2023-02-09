::create docker network for container connect to kafka
docker network create -d bridge kafka-network
docker-compose -f ./kafka/docker-compose.yml up -d

::sleep 15s for kafka init topic
ping 127.0.0.1 -n 16 > nul

::create kafka topic
docker-compose -f ./kafka/docker-compose.yml exec kafka /usr/bin/kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic test1
docker-compose -f ./kafka/docker-compose.yml exec kafka /usr/bin/kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic detect


docker-compose -f ./deligator_group/docker-compose.yml up -d
docker-compose -f ./detection_group/docker-compose.yml up -d

::sleep 2s
ping 127.0.0.1 -n 3 > nul

::migration database for deligator
docker-compose -f ./deligator_group/docker-compose.yml exec postgres createdb detectdb -U postgres
docker-compose -f ./deligator_group/docker-compose.yml exec deligator alembic upgrade head

::migration database for detection
docker-compose -f ./detection_group/docker-compose.yml exec detect_face alembic upgrade head


::sleep 3s
ping 127.0.0.1 -n 4 > nul

docker-compose -f ./downloader_group/docker-compose.yml up -d
