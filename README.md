# GraphQL Gateway Service

## Requirements

* [Docker](https://www.docker.com/).
* [Poetry](https://python-poetry.org/) for Python package and environment management.

## Local Development
* Configure the environment variables:
```bash
cp .example.env .env
```
Update the .env file with other relevant configurations.

* Build the Docker image
```bash
docker compose -f docker-compose.local.yml build --build-arg ENVIRONMENT=dev
```
ENVIRONMENT: `dev`, `stag`, `prod`

* Run the Docker container
```bash
docker compose -f docker-compose.local.yml up -d
```

* Now you can open your browser and interact with these URLs:

Backend, JSON based web API based on OpenAPI: http://localhost:8000/redoc/

Automatic interactive documentation with Swagger UI (from the OpenAPI backend): http://localhost:8000/docs

**Note**: The first time you start your stack, it might take a minute for it to be ready. While the backend waits for the database to be ready and configures everything. You can check the logs to monitor it.

To check the logs, run:

```bash
docker compose -f docker-compose.local.yml logs
```

## Local development, additional details

### General workflow

By default, the dependencies are managed with [Poetry](https://python-poetry.org/), go there and install it.

You can install all the dependencies with:

```console
$ poetry install
```

Then you can start a shell session with the new environment with:

```console
$ poetry shell
```
Make sure your editor is using the correct Python virtual environment.

FastAPI dev run

```console
$ fastapi dev src/app/main.py
```

### Backend tests

### Migrations

As during local development your app directory is mounted as a volume inside the container, you can also run the migrations with `alembic` commands inside the container and the migration code will be in your app directory (instead of being only inside the container). So you can add it to your git repository.

Make sure you create a "revision" of your models and that you "upgrade" your database with that revision every time you change them. As this is what will update the tables in your database. Otherwise, your application will have errors.

* Start an interactive session in the backend container:

```console
$ docker compose -f docker-compose.local.yml exec app bash
```

* After changing a model (for example, adding a column), inside the container, create a revision, e.g.:

```console
$ alembic revision --autogenerate -m "Add column last_name to User model"
```

* Commit to the git repository the files generated in the alembic directory.

* After creating the revision, run the migration in the database (this is what will actually change the database):

```console
$ alembic upgrade head
```

