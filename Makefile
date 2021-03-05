container = documentaries
folder = documentaries

init:
	docker-compose -f compose/docker-compose.yaml build
	make migrate
	make crawl

test:
	docker-compose -f compose/docker-compose.yaml run $(container) python manage.py test

lint:
	docker-compose -f compose/docker-compose.yaml run $(container) pylint documentaries web --ignore=migrations

requirements:
	docker-compose -f compose/docker-compose.yaml run $(container) pip freeze > ${PWD}/$(folder)/requirements.txt

up:
	docker-compose -f compose/docker-compose.yaml up --remove-orphans

down:
	docker-compose -f compose/docker-compose.yaml down --remove-orphans

ssh:
	docker-compose -f compose/docker-compose.yaml run $(container) bash

migrate:
	docker-compose -f compose/docker-compose.yaml run $(container) python manage.py makemigrations
	docker-compose -f compose/docker-compose.yaml run $(container) python manage.py migrate

crawl:
	docker-compose -f compose/docker-compose.yaml run $(container) python manage.py crawl --documentarymania
	docker-compose -f compose/docker-compose.yaml run $(container) python manage.py crawl --documentarytube
	docker-compose -f compose/docker-compose.yaml run $(container) python manage.py crawl --documentaryaddict