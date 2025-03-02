# Makefile for Wagyu Sports

.PHONY: install test pytest clean examples verify

# Install the package in development mode
install:
	pip install -e . -f build/

# Install dependencies
deps:
	pip install -r build/requirements.txt

# Run pytest
test:
	pytest --rootdir=. -c config/pytest.ini

# Run pytest with verbose output
pytest-v:
	pytest --rootdir=. -c config/pytest.ini -v

# Run the example scripts
examples:
	python examples/example.py

# Run the advanced example script
advanced:
	python examples/advanced_example.py

# Verify installation
verify:
	python examples/verify_install.py

# Fetch NBA odds example
fetch-nba:
	python examples/fetch_nba_odds.py

# Clean up build artifacts
clean:
	rm -rf dist/
	rm -rf *.egg-info/
	find . -name "__pycache__" -type d -exec rm -rf {} +
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	find . -name "*.pyd" -delete
	rm -rf test_outputs/

# Build the package
build:
	python build/setup.py sdist bdist_wheel

# Help command
help:
	@echo "Available commands:"
	@echo "  make install   - Install the package in development mode"
	@echo "  make deps      - Install dependencies"
	@echo "  make test      - Run pytest"
	@echo "  make pytest-v  - Run pytest with verbose output"
	@echo "  make examples  - Run the basic example script"
	@echo "  make advanced  - Run the advanced example script"
	@echo "  make verify    - Verify installation"
	@echo "  make fetch-nba - Run the NBA odds example"
	@echo "  make clean     - Clean up build artifacts"
	@echo "  make build     - Build the package"
