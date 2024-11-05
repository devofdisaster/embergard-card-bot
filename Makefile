# Variables
VENV_DIR = .venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip

all: help

$(VENV_DIR):
	python3 -m venv $(VENV_DIR)

install: $(VENV_DIR)
	$(PIP) install -r requirements.txt

test: $(VENV_DIR)
	$(PYTHON) -m unittest discover -s tests

lint: $(VENV_DIR)
	$(PIP) install flake8
	$(VENV_DIR)/bin/flake8 src tests

clean:
	rm -rf $(VENV_DIR)
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

help:
	@echo "Usage:"
	@echo "  make install   - Set up the virtual environment and install dependencies"
	@echo "  make test      - Run tests"
	@echo "  make lint      - Lint the code"
	@echo "  make clean     - Clean up generated files"
	@echo "  make help      - Show this help message"