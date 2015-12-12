install:
	@echo Installing Dependencies
	@pip install -r requirements.txt

run:
	@python runserver.py

lint:
	@sh bin/lint.sh
	@python bin/lint.py

grun:
	@gunicorn -c gunicorn.conf runserver:app

loc:
	@git ls-files | xargs cat | wc -l

loc-desc:
	@git ls-files | xargs wc -l
