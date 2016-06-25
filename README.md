# FLAPY_AUTH
[![Build Status](https://travis-ci.org/maxnovais/flapy_auth.svg?branch=master)](https://travis-ci.org/maxnovais/flapy_auth) 
[![Requirements Status](https://requires.io/github/maxnovais/flapy_auth/requirements.svg?branch=master)](https://requires.io/github/maxnovais/flapy_auth/requirements/?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/maxnovais/flapy_auth/badge.svg?branch=master)](https://coveralls.io/github/maxnovais/flapy_auth?branch=master)
[![Code Health](https://landscape.io/github/maxnovais/flapy_auth/master/landscape.svg?style=flat)](https://landscape.io/github/maxnovais/flapy_auth/master)

Simple auth with great idea


## Motivation
In any project, we want to know who are our users and create for them a unique experience, one of the ability to promote that is signing them.
For this concept was born this project, which can be the basis for any system that requires authentication via login/email and password.


## Technologies
- Python
- Flask
- Docker
- PostgreSQL
- Swagger Specs
- Pytest


### How To Use
#### Preparing enviroment
1. Clone this project `$ git clone https://github.com/maxnovais/flapy_auth.git`
2. Enter in project `$ cd flapy_auth`
3. Create virtual-env using Python3
4. Install requirements `$ pip install -r requirements/dev.txt`
5. Use example config `$ cp auth/config/local.py.example auth/config/local.py`

#### Create Schema
6. Start service for `PostgreSQL`. **Optional:** You can use docker-compose `# docker-compose up -d`
7. Run upgrade using manager `python manage.py db upgrade`
8. Runserver with `python manage.py runserver`


### Tests and Coverage
All tests use Pytest and can be tested using magic `$ make`, for coverage `$ make coverage`



