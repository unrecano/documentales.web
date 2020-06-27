container = kirana
folder = kirana
heroku_app = kiranaweb

deploy:
	cp -R $(folder) ~/
	docker-compose run $(container) pip freeze > ~/$(folder)/requirements.txt
	cd ~/$(folder) && echo 'web: gunicorn kirana.wsgi --workers=2 --bind=0.0.0.0:$$PORT' > Procfile \
					&& git init \
					&& heroku git:remote -a $(heroku_app) \
					&& git add . \
					&& git commit -am "deploy" \
					&& git push heroku master -f \
					&& heroku ps:scale web=1 \
					&& heroku run python manage.py migrate
	sudo rm -r ~/$(folder)
