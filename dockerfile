# this Dockerfile has not been fully completed and tested in dev env.
# Use an official Python runtime as a parent image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
# RUN apt-get update && apt-get install -y netcat-openbsd
# Install system dependencies, UnixODBC for

RUN apt-get update && apt-get install -y gnupg2 unixodbc-dev curl apt-transport-https libgssapi-krb5-2

# Install Microsoft ODBC Driver for SQL Server
RUN curl https://packages.microsoft.com/keys/microsoft.asc |  tee /etc/apt/trusted.gpg.d/microsoft.asc
# Replace 'debian_version' with the correct version number for your base image. debian_version can be 8, 9,10, 11, 12.
# debian_version 11 works for native M1 chip build. if i need to build for platform , like (windows amd64), change to debian_version 10.
RUN curl https://packages.microsoft.com/config/debian/11/prod.list |  tee /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update && apt-get upgrade -y
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql18 
RUN ACCEPT_EULA=Y apt-get install -y mssql-tools18 
RUN echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc

# install ping command, debian-version
RUN apt-get update && apt-get install -y iputils-ping


# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# in COPY commands refers to the current directory in the context of the Docker build (which is /app due to WORKDIR /app).
COPY . .

# Expose port 8000
EXPOSE 8000

# Run the application
CMD ["daphne","-b", "0.0.0.0", "-p", "8000", "automanshop.asgi:application"]