run:
	python3 manage.py runserver
	
migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate

user:
	python3 manage.py createsuperuser

test:
	./manage.py test
	
start:
	django-admin startproject main .

pull_master:
	git add .
	git commit -m 'origin commit'
	git pull origin master

pull_baha:
	git add .
	git commit -m 'baha commit'
	git pull origin baha

celery:
	celery -A main worker -l debug

celery_beat:
	celery -A main beat

restart:
	sudo systemctl daemon-reload
	sudo systemctl restart gunicorn
	sudo nginx -t && sudo systemctl restart nginx

restart_celery:
	sudo supervisorctl reread
	sudo supervisorctl update
	sudo supervisorctl
	
