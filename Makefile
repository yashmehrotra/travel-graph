install:
	@echo Installing Dependencies
	@pip install -r requirements.txt

run:
	@python app.py

lint:
	@sh bin/lint.sh

start_db:
	@../../neo4j-community-2.1.6/bin/neo4j start

stop_db:
	@../../neo4j-community-2.1.6/bin/neo4j stop