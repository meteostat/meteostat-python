PACKAGE_NAME = meteostat

.PHONY: all help lint tests run

all: help

help: ## Show this help
	@echo 'Usage: make COMMAND'
	@echo
	@echo "Commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

lint: ## Run black, pylint and flake8
	black --check $(PACKAGE_NAME) ./tests
	pylint $(PACKAGE_NAME)
	flake8 $(PACKAGE_NAME)

tests: ## Run tests with coverage and linting
	pytest --version
	pytest tests/ --log-cli-level=INFO --cov-branch --cov=$(PACKAGE_NAME) --cov-report xml

format: ## Format the Python code using black
	black $(PACKAGE_NAME)
	black tests/