FROM python:3.10-slim

RUN apt update && apt install -y gcc python3-dev
RUN pip install -U pip setuptools wheel poetry

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

# RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
COPY requirements.txt /app/
RUN pip install -r requirements.txt


COPY ./src ./src
COPY ./.env ./.env

CMD ["uvicorn", "src.app.main:app", "--port", "8000", "--host", "0.0.0.0", "--reload"]