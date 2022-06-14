# Lightweight linux-version of Python with minimal dependencies
FROM python:3.9-alpine3.13
# Defining who maintains the site
LABEL maintainer='Evan Kiolbassa'
# Specifying that the python will not be buffered
ENV PYTHONBUFFERED 1

# Copies the Python specifications from local machine into container directory
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
# Copying the app directory into the container
COPY ./app /app
WORKDIR /app
# Exposing port 8000
EXPOSE 8000

ARG DEV=false

# Run command for the alpine image that was built in the FROM command
# Creates a virtual environment to mitigate the risk of dependency issues
RUN python -m venv /py && \
    # Upgrading the package download manager inside the container virtual environment
    /py/bin/pip install --upgrade pip && \
    # Required for psycopg2 to connect to postgres database
    # apk is Alpine-Package-Keeper
    apk add --update --no-cache postgresql-client && \
    # Groups virtual dependencies into the variable specified below
    apk add --update --no-cache --virtual .tmp-build-deps \
        # Installing packages required for psycopg2 build
        build-base postgresql-dev musl-dev && \
    # Uses pip to install requirements from the .txt file
    /py/bin/pip install -r /tmp/requirements.txt && \
    # A shell script if conditional statement. Note the syntax structure
    if [ $DEV = 'true' ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    # Removal of the tmp directory to make container lightweight.
    # Keeping this directory could lead to future dependency issues
    # that can be mitigated by the directory removal
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    # Adds a custom user that is not the ROOT_USER of the image
    # DO NOT USE ROOT USER
    adduser \
        --disabled-password \
        --no-create-home \
        django-user
# Defines the directory in the container where executables can be run
ENV PATH="/py/bin:$PATH"

USER django-user