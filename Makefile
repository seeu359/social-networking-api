run:
	python -m uvicorn api.main:app --reload

sort:
	poetry run isort .