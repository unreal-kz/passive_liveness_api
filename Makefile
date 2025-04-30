lint:
	pre-commit run --all-files

format:
	black .
	isort .

check:
	ruff .

pytest:
	pytest

test: pytest

docker:
	docker build .
