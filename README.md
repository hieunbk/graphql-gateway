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

* Generate requirements.txt from poetry
```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

* Build the Docker image
```bash
docker build -t <tag-name> -f Dockerfile .
```

* Run the Docker container
```bash
docker run -p 8000:8000 <tag-name>
```

* Now you can open your browser and interact with these URLs:

Backend, JSON based web API based on OpenAPI: http://localhost:8000/redoc/

Automatic interactive documentation with Swagger UI (from the OpenAPI backend): http://localhost:8000/docs

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
* After changing a model (for example, adding a column), inside the container, create a revision, e.g.:

```console
$ alembic revision --autogenerate -m "Add column last_name to User model"
```

* Commit to the git repository the files generated in the alembic directory.

* After creating the revision, run the migration in the database (this is what will actually change the database):

```console
$ alembic upgrade head
```

