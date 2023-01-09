run:
	python -m uvicorn api.main:app --reload

sort:
	poetry run isort .

lint:
	poetry run flake8

test:
	poetry run pytest tests

install:
	poetry install

test-coverage:
	poetry run pytest --cov=api tests/ --cov-report xml
