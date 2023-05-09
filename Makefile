
default: build createdb run

run:
	@echo "Running final.py"
	. venv/bin/activate && streamlit run final.py

createdb:
	@echo "Creating database..."
	. venv/bin/activate && python3 -m createdb


test: build
	@echo "Running tests..."
	. venv/bin/activate && python3 -m unittest discover -v

clean:
	@echo "Cleaning up"
	rm -f ecsel_database.db
	rm -rf venv
	rm -f test_assets/fake_database.db
	rm -rf __pycache__

build:
	@echo "Creating venv"
	test -d venv || python3 -m venv venv
	@echo "Installing requirements..."
	. venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt