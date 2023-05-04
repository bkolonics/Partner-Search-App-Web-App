



createdb:
	@echo "Creating database..."
	python3 -m createdb


test:
	@echo "Running tests..."
	python3 -m unittest discover -v