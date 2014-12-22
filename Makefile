install:
	@echo Installing Dependencies
	@pip install -r requirements.txt

run:
	@python app.py

lint:
	@sh bin/lint.sh

graph_db:
	@sh bin/graph_db.sh