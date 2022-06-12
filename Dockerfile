# Lightweight linux-version of Python with minimal dependencies
FROM python:3.9-alpine3.13
# Defining who maintains the site
LABEL maintainer='Evan Kiolbassa'
# Specifying that the python will not be buffered
ENV PYTHONBUFFERED 1

# Copies the Python specifications from local machine into container directory
COPY ./requirements.txt /tmp/requirements.txt
# Copying the app directory into the container
COPY ./app /app
WORKDIR /app
# Exposing port 8000
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/py/bin:$PATH"

USER django-user