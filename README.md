# 🔫 Hostdog-API 💻

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
PASSWORD={your_postgreSQL_password}
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
