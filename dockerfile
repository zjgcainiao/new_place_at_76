# this Dockerfile has not been fully completed and tested in dev env.
# Use an official Python runtime as a parent image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app


# 
Add . /app/
# Install system dependencies
# RUN apt-get update && apt-get install -y netcat
RUN apt-get update && apt-get install -y netcat-openbsd

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /app/

# Collect static files. skipped due to environemtn variable cannot be read
# RUN python manage.py collectstatic --noinput 

# Expose port 8000
EXPOSE 8000

# Run the application
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "automanshop.asgi:application"]
