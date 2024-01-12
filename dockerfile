# this Dockerfile has not been fully completed and tested in dev env.
# Use an official Python runtime as a parent image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/opt/mssql-tools18/bin:${PATH}"

# Set work directory to /app. the current directory in the context of the Docker build (which is /app due to WORKDIR /app).
WORKDIR /app

# Install system dependencies
# RUN apt-get update && apt-get install -y netcat-openbsd
# Install system dependencies, UnixODBC for

# RUN apt-get update && apt-get install -y gnupg2 unixodbc-dev curl apt-transport-https libgssapi-krb5-2

# # Install Microsoft ODBC Driver for SQL Server
# RUN curl https://packages.microsoft.com/keys/microsoft.asc |  tee /etc/apt/trusted.gpg.d/microsoft.asc

# RUN curl https://packages.microsoft.com/config/debian/10/prod.list |  tee /etc/apt/sources.list.d/mssql-release.list
# RUN apt-get update && apt-get upgrade -y
# RUN ACCEPT_EULA=Y apt-get install -y msodbcsql18 
# RUN ACCEPT_EULA=Y apt-get install -y mssql-tools18 
# RUN echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc

# # install ping command, debian-version
# RUN apt-get update && apt-get install -y iputils-ping

# Replace 'debian_version' with the correct version number for your base image. debian_version can be 8, 9,10, 11, 12.
# debian_version 11 works for native M1 chip build. web:v1 works for native M1 chip build.
# if i need to build for platform , like (windows amd64), change to debian_version `10`.
# Install dependencies in a single RUN layer to reduce image layers
RUN apt-get update && apt-get install -y \
    gnupg2 \
    unixodbc-dev \
    curl \
    apt-transport-https \
    libgssapi-krb5-2 \
    # install ping command, debian-version
    # iputils-ping \ 
    && curl https://packages.microsoft.com/keys/microsoft.asc | tee /etc/apt/trusted.gpg.d/microsoft.asc \
    && curl https://packages.microsoft.com/config/debian/10/prod.list | tee /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && apt-get upgrade -y \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 mssql-tools18 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/* \
    && find / -type f -name "*.pyc" -exec rm -f {} \;

# in COPY commands refers to the current directory in the context of the Docker build (which is /app due to WORKDIR /app).
# Copy the rest of the application code
COPY . .


# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt


# Clean up after package installations
# RUN apt-get clean
# RUN rm -rf /var/lib/apt/lists/*
# # can clear the Python bytecode cache (.pyc files) to save space:
# RUN find / -type f -name "*.pyc" -exec rm -f {} \;
# RUN rm -rf /tmp/*


# Expose port 8000
EXPOSE 8000

# Run the application. 
RUN chmod +x scripts/web_pod_entrypoint.sh

# # Create a non-root user for running the application (security best practice)
# RUN groupadd celerygroup && useradd -r -g celerygroup celeryuser

# # Change ownership of the application files to the non-root user
# RUN chown -R celeryuser:celerygroup /app

# # Run the application as a non-root user
# USER celeryuser
# Give execute permissions to the entrypoint script
# RUN chmod -R +x /scripts


# Set the script as the entrypoint. Set the script as the entrypoint
ENTRYPOINT ["scripts/web_pod_entrypoint.sh"]

# CMD ["daphne","-b", "0.0.0.0", "-p", "8000", "automanshop.asgi:application"]