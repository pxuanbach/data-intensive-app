docker-compose -f ./deligator_group/docker-compose.yml exec postgres createdb app -U postgres
docker-compose -f ./deligator_group/docker-compose.yml exec postgres createdb detectdb -U postgres
docker-compose -f ./deligator_group/docker-compose.yml exec deligator alembic upgrade head
docker-compose -f ./detection_group/docker-compose.yml exec detect_face alembic upgrade head