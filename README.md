# 🔫 Hostdog-API 💻
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/dwyl/esta/issues)
[![start with why](https://img.shields.io/badge/start%20with-why%3F-brightgreen.svg?style=flat)](http://www.ted.com/talks/simon_sinek_how_great_leaders_inspire_action)

## Setup
clone repository
```sh
$ git clone https://github.com/Hostdogs/Hostdog-Backend.git
$ cd Hostdog-Backend
```
virtual environment
```sh
$ pip install virtualenv
```
```sh
$ virtualenv <name>
$ source <name>/Scripts/activate
```
dependencies
```sh
(venv)$ pip install -r requirements.txt
```
.env
```
SECRET_KEY={your_secret_key}
PASSWORD={your_postgreSQL_password)
```
test
```sh
(venv)$ py manage.py runserver
```

## Celery
### Worker
```sh
(venv)$ celery -A backend worker -l info --pool=solo
```

### Beat
```sh
(venv)$ celery -A backend beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
```
