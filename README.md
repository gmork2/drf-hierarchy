# drf-hierarchy

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Build Status](https://travis-ci.com/gmork2/drf-hierarchy.svg?branch=master)](https://travis-ci.com/gmork2/drf-hierarchy)

This app implements a modified preorder tree traversal with django groups
in order to provide permissions inheritance.

Set up the project with uv:

```shell script
cp .env.example .env
uv sync --group dev
uv run python manage.py migrate
uv run python manage.py createsuperuser
uv run python manage.py runserver 0.0.0.0:8000
```

Useful development commands:

```shell script
uv run pytest
uv run ruff check .
uv run python manage.py check --deploy --settings=sample.settings
```

Docker workflow (legacy):

```shell script
docker-compose up -d
docker-compose exec drf-hierarchy python3 manage.py createsuperuser
x-www-browser 0.0.0.0:8000/admin
x-www-browser 0.0.0.0:8000
```
