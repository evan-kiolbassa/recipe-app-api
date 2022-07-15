# recipe-app-api

Django RESTFUL API developed using the
test-driven deployment methodology.

Testing and linting is triggered each time a push is made to the code repository
to maintain quality of source-code.

Linting is based upon flake8 formatting standards.

Running this API requires the installation of Docker.

Running docker-compose commands will install all of the necessary app dependencies;

```
docker-compose build
docker-compose up
```

The Dockerfile is combined to run in the local development environment.

To see the Swagger documentation for the API, enter the following URL into your browser;

```
http://127.0.0.1:8000/api/docs
```

Admin Interface:
```
http://127.0.0.1:8000/admin/
```
