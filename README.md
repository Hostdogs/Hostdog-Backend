# 🔫 Hostdog-API 💻
[![Build Status](https://travis-ci.org/Hostdogs/Hostdog-Backend.png?branch=main)](https://travis-ci.org/Hostdogs/Hostdog-Backend)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/dwyl/esta/issues)
[![start with why](https://img.shields.io/badge/start%20with-why%3F-brightgreen.svg?style=flat)](http://www.ted.com/talks/simon_sinek_how_great_leaders_inspire_action)

## Requirements
- PostgreSQL : สร้าง new database ชื่อ Hostdog
- Redis 
- Python3
- Django 3.2
## Setup
เริ่มจากการ clone repository นี้ก่อน
```sh
$ git clone https://github.com/Hostdogs/Hostdog-Backend.git
$ cd Hostdog-Backend
```
ติดตั้ง virtual environment
```sh
$ pip install virtualenv
```
ทำการสร้าง virtual environment เพื่อติดตั้ง dependencies แล้ว Activate
```sh
$ virtualenv <name>
$ source <name>/Scripts/activate
```
ติดตั้ง dependencies
```sh
(venv)$ pip install -r requirements.txt
```
สร้างไฟล์ .env
```
SECRET_KEY={your_secret_key}
PASSWORD={your_postgreSQL_password)
```
หลังจากนั้น
```sh
(venv)$ py manage.py runserver
```
สามาารถเข้าไปทดสอบได้ที่ ``` http://127.0.0.1:8000 ```

## Celery
### Worker
```sh
(venv)$ celery -A backend worker -l info --pool=solo
```

### Beat
```sh
(venv)$ celery -A backend beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
```
