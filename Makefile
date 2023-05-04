
default: build createdb run

run:
	@echo "Running final.py"
	python3 final.py


createdb:
	@echo "Creating database..."
	python3 -m createdb


test:
	@echo "Running tests..."
	python3 -m unittest discover -v

clean:
	@echo "Cleaning up"
	rm -f ecsel_database.db
	rm -rf venv

build:
	@echo "Creating venv"
	test -d venv || python3 -m venv venv
	. venv/bin/activate
	@echo "Installing requirements..."
	pip3 install -r requirements.txt