container = kirana
folder = kirana
heroku_app = kiranaweb

deploy:
	cp -R $(folder) ~/
	docker-compose run $(container) pip freeze > ~/$(folder)/requirements.txt
	cd ~/$(folder) && echo 'web: python manage.py runserver 0.0.0.0:$$PORT' > Procfile \
					&& git init \
					&& heroku git:remote -a $(heroku_app) \
					&& git add . \
					&& git commit -am "deploy" \
					&& git push heroku master -f \
					&& heroku ps:scale web=1
	sudo rm -r ~/$(folder)