# recipe-app-api

Django RESTFUL API developed using the
test-driven deployment methodology.

Testing and linting is triggered each time a push is made to the code repository
to maintain quality of source-code.

Running this API requires the installation of Docker.

Running docker-compose commands will install all of the necessary app dependencies;

```
docker-compose build
docker-compose up
```bash

To run the API, copy and paste the following command into your terminal;

```
docker-compose run --rm app sh -c 'python manage.py startapp user'
```bash

