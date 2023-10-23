# theatre-api-service
Theatre API Service is a backend implementation designed to support theatre-related applications. This service provides comprehensive API endpoints to manage various aspects of theatre data, including genres, actors, theatre halls, plays, performances, and reservations. It's built to facilitate easy access and management of theatre-related information for your application.
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

#### Documentation
For detailed information and API documentation, visit:
http://127.0.0.1:8088/api/doc/swagger/

#### Test admin
You can use the following credentials to access the admin panel for testing purposes:
```shell
email: theatre@admin.com
password: 9900py
```
Available API Endpoints
```shell
Create a user: api/user/register
View your profile: api/user/me
Get an access token: api/user/token
Refresh an access token: api/user/token/refresh
Verify an access token: api/user/token/verify
```
## Features
- JWT Authenticated
- Managing  reservation of tickets in the theatre
- Documentation is located in /api/doc/swagger/
- Opportunity to upload images to Play
- For user identification, we use email addresses instead of username


## DB structure
Here is an overview of the project's database structure:


![demo](..%2F..%2FDesktop%2FScreenshot%202023-10-20%20at%2019.06.34.png)