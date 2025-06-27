.PHONY: help install install-dev test lint format type-check clean build

help:
	@echo "Available commands:"
	@echo "  make install      - Install core dependencies"
	@echo "  make install-dev  - Install development dependencies"
	@echo "  make test         - Run tests with coverage"
	@echo "  make lint         - Run linting checks"
	@echo "  make format       - Format code with black"
	@echo "  make type-check   - Run type checking with mypy"
	@echo "  make clean        - Remove build artifacts and cache"
	@echo "  make build        - Build distribution packages"

install:
	pip install -r requirements.txt
	pip install -e .

install-dev:
	pip install -r requirements-dev.txt
	pip install -e .
	pre-commit install

test:
	pytest

lint:
	ruff check .

format:
	black src tests
	ruff check . --fix

type-check:
	mypy src

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build