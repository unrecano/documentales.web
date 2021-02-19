container = kirana
folder = kirana
heroku_app = kiranaweb

deploy:
	cp -R $(folder) ~/
	cd compose && docker-compose run $(container) pip freeze > ~/$(folder)/requirements.txt
	cd ~/$(folder) && echo 'web: gunicorn kirana.wsgi --workers=2 --bind=0.0.0.0:$$PORT' > Procfile \
					&& git init \
					&& heroku git:remote -a $(heroku_app) \
					&& git add . \
					&& git commit -am "deploy" \
					&& git push heroku master -f \
					&& heroku ps:scale web=1 \
					&& heroku run python manage.py migrate --app=$(heroku_app)
	sudo rm -r ~/$(folder)

init:
	cd compose && docker-compose build
	cd compose && docker-compose run $(container) python manage.py migrate
	cd compose && docker-compose run $(container) python manage.py loaddata documentaries sites

test:
	cd compose && docker-compose run $(container) python manage.py test

lint:
	cd compose && docker-compose run $(container) pylint documentaries kirana

requirements:
	cd compose && docker-compose run $(container) pip freeze > ${PWD}/$(folder)/requirements.txt

up:
	cd compose && docker-compose up

down:
	cd compose && docker-compose down --remove-orphans