# 🔫 Hostdog-API 💻
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
หลังจากนั้น
```sh
(venv)$ py manage.py runserver
```
สามาารถเข้าไปทดสอบได้ที่ ``` http://127.0.0.1:8000 ```
