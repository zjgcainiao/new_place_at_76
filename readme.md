# Python-based integrated automotive repair shop management system

Copyright (C) Yin Wang 2023-2024 (info@76prolubeplus.com).
_last updated: Jan 2024_

## 0. Prerequisites

`Django framework v4.2` + `Daphne v4.0` + `Microsoft SQL Server 2019`. Provides API capablities for future frontend web application and mobile application.

1. python 3.10
2. django 4.2.9
3. django REST framework 3.14.0
4. daphne 4.0.0
5. ms sql server 2022. recommend to use docker image `mcr.microsoft.com/mssql/server:2022-latest` to run ms sql server. For Apple M1, M2 chip based environment, please use `mcr.microsoft.com/azure-sql-edge` instead.

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

Before running the server, find the file name `env.example` and rename it to `.env`. Then, update the `.env` file with your own database information.

```zsh
#!/bin/bash

# Define the file names
source_file="env.example"
destination_file=".env"

# Check if the source file exists and is not a directory
if [ -f "$source_file" ]; then
    # Rename the file
    mv "$source_file" "$destination_file"
    echo "File renamed successfully."
else
    # Error message if file does not exist or is a directory
    echo "Error: '$source_file' does not exist or is a directory."
fi


```

- Use the [command listed here](https://gist.github.com/barbietunnie/d83c4bb7c0eb2ee4e3e71f91697a68f6) to generate a new secret key for the django project.

- AI assistant capablity (aka, Pulido) requires a chatGPT API key. Please contact the author for more information.

### Dockerized deployment

To test dockierized deployment, please run the following commands:

```zsh

# build docker image starting from the root of the project folder.
# please make sure the .env file is in the root of the project folder. use the env.example as a template.
docker buildx build -t myapp:latest .
docker rm -f local-myapp || true && \
docker run -p 8000:8000 --env-file .env --name local-myapp myapp:latest daphne -b 0.0.0.0 -p 8000 automanshop.asgi:application
```

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
- provides real-time webSocket-based chatting capablities to facilitate the communication between the customer and the employee, especially when the customer is waiting for the repair to be done and we need to ask the customer for additional information.

## 2. System Architecture

[coming soon]
