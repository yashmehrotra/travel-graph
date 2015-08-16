install:
	@echo Installing Dependencies
	@pip install -r requirements.txt

run:
	@python runserver.py

lint:
	@sh bin/lint.sh

grun:
	@gunicorn -c gunicorn.conf yashrun:app

client:
	@nodejs client_app/app.js
