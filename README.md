# drf-hierarchy

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

This app implements a modified preorder tree traversal with django groups
in order to provide permissions inheritance. 

```shell script
docker-compose up -d
docker-compose exec drf-hierarchy python3 manage.py createsuperuser
x-www-browser 0.0.0.0:8000/admin
x-www-browser 0.0.0.0:8000
```
