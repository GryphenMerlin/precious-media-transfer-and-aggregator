.PHONY: help install test run-cli run-gui clean lint format

help:
	@echo "Precious Media Transfer and Aggregator - Available Commands"
	@echo ""
	@echo "install        Install dependencies"
	@echo "test           Run test suite"
	@echo "test-cov       Run tests with coverage report"
	@echo "run-cli        Run CLI interface"
	@echo "run-gui        Run GUI interface"
	@echo "lint           Run code linter (flake8)"
	@echo "format         Format code (black)"
	@echo "type-check     Run type checking (mypy)"
	@echo "clean          Remove cache and build artifacts"

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=src --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

run-cli:
	python src/main.py --help

run-gui:
	python src/gui.py

lint:
	flake8 src/ tests/ --max-line-length=100

format:
	black src/ tests/ --line-length=100

type-check:
	mypy src/ --ignore-missing-imports

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
