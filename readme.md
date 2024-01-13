# Python-based integrated automotive repair shop management system

## 0. Prerequisites

`Django framework v4.2` + `Daphne v4.0` + `Microsoft SQL Server 2019`. Provides API capablities for future frontend web application and mobile application.

1. python 3.10 or later
2. django 4.2.9 or later
3. daphne 4.0.0 or later
4. ms sql server 2019 or later. recommend to use docker image `mcr.microsoft.com/mssql/server:2019-latest` to run ms sql server.

4.2.9 Django framework + Daphne + Microsoft SQL Server.

```zsh
# create new virtual environment
python -m venv myenv
# activating new virtual environment
source myenv/bin/activate
# install required packages
pip install --upgrade pip
pip install -r requirements.txt

# make database migrations
python manage.py makemigrations
python manage.py migrate

# test run on http://127.0.0.1:8000
python manage.py runserver


# generate self-signed certificate
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365
# test running on https protocol
python manage.py runsslserver 8443 \
--certificate cert.pem \
--key key.pem

```

AI assistant capablity (aka, Pulido) requires a chatGPT API key. Please contact the author for more information.

To test dockierized deployment, please run the following commands:

```zsh

# build docker image starting from the root of the project folder.
# please make sure the .env file is in the root of the project folder. use the env.example as a template.
docker buildx build -t myapp:latest .
docker rm -f local-myapp || true && \
docker run -p 8000:8000 --env-file .env --name local-myapp myapp:latest daphne -b 0.0.0.0 -p 8000 automanshop.asgi:application
```

Copyright (C) Yin Wang 2023-2024 (info@76prolubeplus.com).
_last updated: Jan 2024_

## 1. Introduction

A data-driven, full-fledging automotive repair shop management system, including:

1. Customer management
2. appiontment management
3. repair order management
4. vehicle information management and smart diagnosis
5. inventory management
6. accounting management
7. Talent management
8. user management
9. report management
10. shift management
11. AI-based functions: virtual assistant, smart diagnosis, smart license plate recognition etc.

- An authorized employee user can access the centralized dashboard to manage daily operations, such as creating a new repair order, adding a new customer, checking existing inventory, etc. Daily operation-required functions are integrated into an centralized dashboard.
- Talent management system, or employee management system has a separate dashboard for HR to manage employee information, such as adding a new employee, checking employee attendance, etc. Only authorized HR user can access the talent management system. Each employee has access to check his/her own HR profile, including hours worked, and salary information.
- user management system is responsible to handle two types of user accounts: employee user account and customer user account. Employee user account is used to access the centralized dashboard, while customer user account is used to access the customer portal.
- provides periodic tasks (`celery`, `celery-beat`) that are scheduled to run at a specific time, such as sending email to remind customer about the upcoming appointment, sending email to remind customer about the upcoming vehicle inspection, etc.
- provides the dockerized capacity to deploy the system on the containers, such as `docker`, `docker-compose`, `kubernetes`, etc.
- provides real-time webSocket-based chat capablities to facilitate the communication between the customer and the employee, especially when the customer is waiting for the repair to be done and we need to ask the customer for additional information.

## 2. System Architecture

[coming soon]
