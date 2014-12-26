install:
	@echo Installing Dependencies
	@pip install -r requirements.txt

run:
	@neo4j-community-2.1.6/bin/neo4j start
	@python app.py

lint:
	@sh bin/lint.sh

stop:
	@neo4j-community-2.1.6/bin/neo4j stop