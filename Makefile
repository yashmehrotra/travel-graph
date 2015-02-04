install:
	@echo Installing Dependencies
	@pip install -r requirements.txt

run:
	@python runserver.py

lint:
	@sh bin/lint.sh
