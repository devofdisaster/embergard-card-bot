# Variables
VENV_DIR = .venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip

all: help

$(VENV_DIR):
	python3 -m venv $(VENV_DIR)

run:
	python3 main.py

install: $(VENV_DIR)
	mkdir logs
	$(PIP) install -r requirements.txt

test: $(VENV_DIR)
	$(PIP) install -r requirements-test.txt
	$(PYTHON) -m pytest

lint: $(VENV_DIR)
	$(PIP) install ruff
	$(VENV_DIR)/bin/ruff check src

clean:
	rm -rf $(VENV_DIR)
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

help:
	@echo "Usage:"
	@echo "  make install       - Set up the virtual environment and install dependencies"
	@echo "  make run           - Start the Card Bot in the foreground"
	@echo "  make test          - Run tests with pytest"
	@echo "  make test-coverage - Run tests with coverage reporting"
	@echo "  make lint          - Lint the code"
	@echo "  make clean         - Clean up generated files"
	@echo "  make help          - Show this help message"