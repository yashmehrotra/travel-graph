install:
	@echo Installing Dependencies
	@pip install -r requirements.txt

run:
	@python runserver.py

lint:
	@sh bin/lint.sh

grun:
	@gunicorn runserver:app -b 0.0.0.0:5000

client:
	@nodejs client_app/app.js
