migrations:
	poetry run python3 -m manage makemigrations

migrate:
	poetry run python3 -m manage migrate

run-server:
	poetry run python3 -m manage runserver

superuser:
	poetry run python3 -m manage createsuperuser

tests:
	poetry run python3 -m manage tests

lint:
	poetry run flake8
