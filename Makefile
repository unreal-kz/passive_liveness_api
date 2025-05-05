PROJECT_NAME := flutter_liveness_verifier
PYTHON_VERSION := 3.9  # Or your preferred Python version

.PHONY: lint test run

lint:
	flake8 src/$(PROJECT_NAME)

test:
	pytest

run:
	uvicorn src/$(PROJECT_NAME).main:app --reload
