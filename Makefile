# Define the name of the Docker container
CONTAINER_NAME=couchdbCompanion

# Command to launch Docker container
.PHONY: start
start:
	@echo "• Launching CouchDB container..."
	@docker run --rm -d -p 5984:5984 -e COUCHDB_USER=admin -e COUCHDB_PASSWORD=password --name $(CONTAINER_NAME) couchdb:3.3.3
	@echo "• Waiting for CouchDB to start..."
	@sleep 7  # Adjust this sleep time if needed
	@echo "• Activating virtual environment"
	@. venv/bin/activate	
	@echo "• Populate the db"
	@PYTHONPATH=$(shell pwd)/app python3 app/scripts/default_db.py

# Command to launch the application
.PHONY: app
app:
	@. venv/bin/activate && PYTHONPATH=$(shell pwd)/app python3 app/run.py

# Command to stop and remove the Docker container
.PHONY: clean
clean:
	@echo "Stopping and removing the CouchDB container..."
	@if [ $$(docker ps -q -f name=$(CONTAINER_NAME)) ]; then \
		docker stop $(CONTAINER_NAME); \
	else \
		echo "Container $(CONTAINER_NAME) is not running."; \
	fi
