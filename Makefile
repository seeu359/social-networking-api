run:
	python -m uvicorn api.main:app --reload

sort:
	poetry run isort .

lint:
	poetry run flake8

test:
	poetry run pytest tests

p_install:
	poetry install

install:
	pip install -r requirements.txt

test-coverage:
	poetry run pytest --cov=api tests/ --cov-report xml
