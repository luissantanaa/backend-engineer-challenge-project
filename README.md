# backend-engineer-challenge-project

## Description

This project exposes an API built with Python, FastAPI, SQLAlchemy and uses a PostgreSQL database. The project has asynchronous endpoints and database sessions and is containerized using Docker with a docker compose file to run.

The service calls an endpoint on an external service which returns data points like the one following:
```
{
    "time": 1713798477,
    "value": [
        157,
        42,
        76,
        190
    ],
    "tags": []
}
```

After receiving this data, the service processes the "time" field into a ISO8601 format timestamp and decodes the "value" array into a float32. It also checks the tags recieved and adds a field depicting whether the data is valid or not.
```
{
    "time": "2024-04-22T15:08:01Z",
    "value": -0.23173533380031586,
    "valid": true,
    "tags": []
}
```

## Docker Utilities

Docker compose: 
```
name: "data-processor"
services:
  postgres:
    image: postgres:16.2-alpine
    container_name: postgres_db
    restart: always
    networks:
      - data-processor
    ports:
      - 5432:5432
    volumes:
      - ./postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    environment:
      - POSTGRES_DB_NAME=${POSTGRES_DB_NAME}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_SERVER=${POSTGRES_SERVER}
      - PGUSER=${PGUSER}
    healthcheck:
      test:
        [
          "CMD-SHELL",
          "pg_isready",
          "-d",
          "${POSTGRES_DB_NAME}",
          "-U",
          "${POSTGRES_USER}"
        ]
      interval: 10s
      timeout: 5s
      retries: 5

  processor:
    container_name: processor
    networks:
      - data-processor
    ports:
      - 8080:8080
    build:
      dockerfile: ./Dockerfile
    depends_on:
      postgres:
        condition: service_healthy
    restart: on-failure

networks:
  data-processor:
    driver: bridge
```

Dockerfile:
```
FROM python:3.10-alpine
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#
WORKDIR /code


COPY ./requirements.txt /code/requirements.txt
COPY ./.env /code/.env

#
RUN pip install --no-cache-dir -r /code/requirements.txt

#
COPY ./app /code/app

#
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

## API Endpoints
The project exposes four endpoints:
```
GET /api/data
GET /api/populate
POST /auth/login
POST /auth/signup
```
The data endpoint returns the data points stored in the database and takes the following optional parameters:
```   
start: datetime
end: datetime
skip: int
limit: int
```
The start and end parameters are used to select the range of data points to be returned to the user.
The skip parameter is used to offset the data points returned and limit limits the number of points.

The populate endpoint performs a call to the external server and adds the returned data to the data base.

The signup endpoint takes a username and a password and creates a user if the username is not taken.
The login endpoint takes a username and a password and returns an access/refresh JWT upon a successful authentication. 



