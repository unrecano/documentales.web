container = documentaries
folder = documentaries
compose-file = compose/docker-compose.yaml

init:
	docker-compose -f $(compose-file) build
	make migrate
	make crawl

test:
	docker-compose -f $(compose-file) run $(container) python manage.py test

lint:
	docker-compose -f $(compose-file) run $(container) pylint documentaries web api --ignore=migrations --disable=duplicate-code

requirements:
	docker-compose -f $(compose-file) run $(container) pip freeze > ${PWD}/$(folder)/requirements.txt

up:
	docker-compose -f $(compose-file) up

build:
	docker-compose -f $(compose-file) build

down:
	docker-compose -f $(compose-file) down

ssh:
	docker-compose -f $(compose-file) run $(container) bash

migrate:
	docker-compose -f $(compose-file) run $(container) python manage.py makemigrations
	docker-compose -f $(compose-file) run $(container) python manage.py migrate

crawl:
	docker-compose -f $(compose-file) run $(container) python manage.py crawl --documentarymania
	docker-compose -f $(compose-file) run $(container) python manage.py crawl --documentarytube
	docker-compose -f $(compose-file) run $(container) python manage.py crawl --documentaryaddict
	docker-compose -f $(compose-file) run $(container) python manage.py crawl --documentarytop
	docker-compose -f $(compose-file) run $(container) python manage.py crawl --documentaryheaven

loaddata:
	docker-compose -f $(compose-file) run $(container) python manage.py loaddata documentaries sites

install:
	docker-compose -f $(compose-file) run $(container) bash -c "pip install $(package) && pip freeze > requirements.txt"
	make build