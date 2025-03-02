# Makefile for Python Odds API Client

.PHONY: install test unittest clean

# Install the package in development mode
install:
	pip install -e .

# Install dependencies
deps:
	pip install -r requirements.txt

# Run the test script
test:
	python run_test.py

# Run unit tests
unittest:
	python test_odds_client.py

# Run the example script
example:
	python example.py

# Run the advanced example script
advanced:
	python advanced_example.py

# Clean up build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -name "__pycache__" -type d -exec rm -rf {} +
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	find . -name "*.pyd" -delete

# Build the package
build:
	python setup.py sdist bdist_wheel

# Help command
help:
	@echo "Available commands:"
	@echo "  make install  - Install the package in development mode"
	@echo "  make deps     - Install dependencies"
	@echo "  make test     - Run the test script"
	@echo "  make unittest - Run unit tests"
	@echo "  make example  - Run the example script"
	@echo "  make advanced - Run the advanced example script"
	@echo "  make clean    - Clean up build artifacts"
	@echo "  make build    - Build the package"
