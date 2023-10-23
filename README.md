# theatre-api-service

## Installation

Python3 must be already installed.
```shell
git@github.com:ZaichenkoViktoriia/theatre-api-service.git
cd theatre_api_service
python3 -m venv venv
source venv/bin/activate  (On Windows use `venv\Scripts\activate`)
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 
```


documentation
http://127.0.0.1:8088/api/doc/swagger/

#### Test admin 
```shell
email: theatre@admin.com
password: 9900py
```
- create user api/user/register
- your profile api/user/me
- get access token api/user/token
- refresh token api/user/token/refresh
- verify token api/user/token/verify


## DB structure
Structure of project

![Screenshot 2023-10-20 at 19.06.34.png](..%2F..%2FDesktop%2FScreenshot%202023-10-20%20at%2019.06.34.png)