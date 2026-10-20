# drf-hierarchy

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Build Status](https://travis-ci.com/gmork2/drf-hierarchy.svg?branch=master)](https://travis-ci.com/gmork2/drf-hierarchy)

`drf-hierarchy` is a reusable Django app that adds **hierarchical group permissions**
on top of Django `auth.Group` using **MPTT** (tree structure).

It is designed for projects where permissions should be inherited through a group tree
(for example: organization units, tenants, folders, or role hierarchies).

## What problem this app solves

By default, Django groups are flat. This app provides:

- A tree model (`MPTTGroup`) that wraps `auth.Group`.
- Permission inheritance across parent/child nodes.
- A DRF endpoint to expose/manage the hierarchy.
- Admin integration with tree visualization.
- Validation guards for circular references and max children constraints.

## Compatibility

- Python: `>=3.10,<3.13`
- Django: `>=4.2,<7.0`
- djangorestframework: `>=3.15,<3.17`
- django-mptt: `>=0.16,<1.0`

Validated test matrix in this repository:

- Django 4.2.x
- Django 5.x
- Django 6.x

## Installation

### Recommended (uv)

```bash
uv add drf-hierarchy
```

For local development of this repository:

```bash
cp .env.example .env
uv sync --group dev
uv run python manage.py migrate
uv run python manage.py createsuperuser
uv run python manage.py runserver 0.0.0.0:8000
```

### Alternative (pip)

```bash
pip install drf-hierarchy
```

## Integrating into an existing Django project

### 1. Add installed apps

```python
INSTALLED_APPS = [
    # ...
    "rest_framework",
    "mptt",
    "hierarchy",
]
```

### 2. Enable authentication backend

```python
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "hierarchy.backends.MPTTGroupBackend",
]
```

`MPTTGroupBackend` augments Django group permission resolution by traversing the hierarchy.

### 3. Run migrations

```bash
python manage.py migrate
```

### 4. Expose API routes (optional but recommended)

```python
from django.urls import path
from rest_framework import routers
from hierarchy.views import MPTTGroupViewSet

router = routers.DefaultRouter()
router.register("hierarchy", MPTTGroupViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
] + router.urls
```

## Configuration

The app supports these settings:

```python
# Traversal method used to compute inherited permissions.
# Must be one of:
# get_ancestors, get_children, get_descendants, get_family,
# get_next_sibling, get_previous_sibling, get_root, get_siblings
HIERARCHY_MPTT_METHOD = "get_descendants"

# Max serialized depth for recursive children in API responses.
HIERARCHY_MAX_SERIALIZATION_DEPTH = 5

# Optional global maximum number of children per node (project-defined usage).
HIERARCHY_MAX_CHILDREN = None
```

Notes:

- `HIERARCHY_MPTT_METHOD` is validated at startup.
- `HIERARCHY_MAX_SERIALIZATION_DEPTH` prevents unbounded recursive payloads.

## Data model and behavior

`MPTTGroup` fields:

- `group` (`OneToOne` with `auth.Group`)
- `parent` (tree parent)
- `inheritable` (whether node permissions are inheritable)
- `max_children` (per-node children limit)
- `active`, `propagate` (state fields)

Validation rules:

- A node cannot be its own parent.
- A node cannot set one of its descendants as parent.
- Parent `max_children` is enforced.

## Security and production guidance

This repository includes a `sample` project for demos/tests.

Before deploying any real project:

- Set `DEBUG=False`.
- Use a strong `SECRET_KEY`.
- Configure `ALLOWED_HOSTS`.
- Enable secure cookies and HTTPS/HSTS settings.
- Run:

```bash
python manage.py check --deploy
```

The included `.env.example` shows secure-related variables you can set.

## Development workflow (this repository)

```bash
uv sync --group dev
uv run ruff check .
uv run pytest
uv run python manage.py check --settings=sample.settings
uv run python manage.py check --deploy --settings=sample.settings
```

## Admin usage

The app registers `MPTTGroup` in Django admin using `DraggableMPTTAdmin`, so the hierarchy can be managed visually.

## API overview

Default `sample` API route:

- `GET /hierarchy/` root hierarchy nodes
- standard DRF `ModelViewSet` actions for CRUD

Access is protected by `DjangoModelPermissions`.

## License

GPLv3. See `LICENSE`.
