install:
	@echo Installing Dependencies
	@pip install -r requirements.txt

run:
	@python app.py

lint:
	@sh lint.sh