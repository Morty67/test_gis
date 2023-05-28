# Django REST API for Geospatial Data Management
This project is the server-side component of a web application that provides an API for managing geospatial data and interacting with a database.

## Technologies Used

*  Backend: Django REST Framework.
*  Database: PostgreSQL with PostGIS extension.


## Installing / Getting started:
```shell
To get started, you need to clone the repository from GitHub: https://github.com/Morty67/test_gis/tree/develop
Python 3 must be installed

cd config
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```
## How to get access

Domain:
*  localhost:8000 or 127.0.0.1:8000

## Features:
*  PostgreSQL database with the PostGIS extension for storing geospatial data.
*  API endpoints for performing CRUD (Create, Read, Update, Delete) operations on places.
*  Endpoint for finding the nearest place to a given coordinate.
*  JSON format for data exchange.
*  Documentation is located at api/doc/swagger/
