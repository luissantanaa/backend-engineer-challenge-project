# backend-engineer-challenge-project

## How to run
In the root directory, run: 
```
docker compose up
```
While running, you can access the /docs endpoint to get the OpenAPI page for the project.

The init.sql file present also creates an admin user automatically. You can use this admin with username:"admin" password:"admin".

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

## API Endpoints
The project exposes four endpoints:
```
GET  /api/data
GET  /api/populate
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
If the endpoint is called by a normal user, then all the data points returned are valid while an admin gets valid and invalid data points.

The populate endpoint performs a call to the external server and adds the returned data to the data base. This endpoint can only be called by an admin.

The signup endpoint takes a username and a password and creates a user if the username is not taken.
The login endpoint takes a username and a password and returns an access/refresh JWT upon a successful authentication. 

## .env file

The project requires a .env file with the following fields:
```
POSTGRES_DB_NAME
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_SERVER
PGUSER

POSTGRES_TEST_DB_NAME

SERVER_URL
SERVER_PORT

ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_MINUTES
JWT_SECRET_KEY
JWT_REFRESH_SECRET_KEY
ALGORITHM
```
Normally, this file would not be present in the repository but in this case it is included for testing purposes.

## Database tables
The project uses the init.sql file to create the databases when initializing the containers for the first time. It creates two databases with the same tables, one for production and one for testing.
```
CREATE DATABASE data_points_db;
\connect data_points_db;

CREATE TABLE "users" (
  "id" serial PRIMARY KEY,
  "username" varchar NOT NULL UNIQUE,
  "hashed_password" varchar NOT NULL,
  "role" varchar NOT NULL DEFAULT 'user'
);

CREATE TABLE "data_points" (
  "id" serial PRIMARY KEY,
  "time" timestamptz NOT NULL,
  "value" DOUBLE PRECISION NOT NULL,
  "valid" boolean NOT NULL,
  "tags" varchar[]
);

INSERT INTO USERS(id, username, hashed_password, role) VALUES(0, 'admin', '$2b$12$a/pMatsPyWuHa5KdqatsFOLZgPYjPZU4If4//jeretXqZ.ujoYFJG','admin');

CREATE DATABASE test_data_points_db;
\connect test_data_points_db;

CREATE TABLE "users" (
  "id" serial PRIMARY KEY,
  "username" varchar NOT NULL UNIQUE,
  "hashed_password" varchar NOT NULL,
  "role" varchar NOT NULL DEFAULT 'user'
);

CREATE TABLE "data_points" (
  "id" serial PRIMARY KEY,
  "time" timestamptz NOT NULL,
  "value" DOUBLE PRECISION NOT NULL,
  "valid" boolean NOT NULL,
  "tags" varchar[]
);

INSERT INTO USERS(id, username, hashed_password, role) VALUES(0, 'admin', '$2b$12$a/pMatsPyWuHa5KdqatsFOLZgPYjPZU4If4//jeretXqZ.ujoYFJG','admin');
```
The "insert" lines create an admin user for testing.

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


## Postman Collection
Besides using the sandbox in /docs, you can also use the following postman collection to test the API. Reminder that the /populate and /data endpoints require a Bearer token obtained from the /login endpoint.

```
{
	"info": {
		"_postman_id": "dc1d2ddc-a7b6-4763-8cae-7ebb59e93f49",
		"name": "Data Points Service",
		"schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
		"_exporter_id": "34499909"
	},
	"item": [
		{
			"name": "POST LOGIN",
			"request": {
				"auth": {
					"type": "noauth"
				},
				"method": "POST",
				"header": [],
				"body": {
					"mode": "urlencoded",
					"urlencoded": [
						{
							"key": "username",
							"value": "admin",
							"type": "text"
						},
						{
							"key": "password",
							"value": "admin",
							"type": "text"
						}
					]
				},
				"url": {
					"raw": "http://localhost:8080/auth/login",
					"protocol": "http",
					"host": [
						"localhost"
					],
					"port": "8080",
					"path": [
						"auth",
						"login"
					],
					"query": [
						{
							"key": "username",
							"value": "admin",
							"disabled": true
						},
						{
							"key": "password",
							"value": "admin",
							"disabled": true
						}
					]
				}
			},
			"response": []
		},
		{
			"name": "POST SIGNUP",
			"request": {
				"method": "POST",
				"header": [],
				"body": {
					"mode": "raw",
					"raw": "{\n    \"username\":\"test\",\n    \"password\":\"test\"\n}",
					"options": {
						"raw": {
							"language": "json"
						}
					}
				},
				"url": {
					"raw": "http://localhost:8080/auth/signup",
					"protocol": "http",
					"host": [
						"localhost"
					],
					"port": "8080",
					"path": [
						"auth",
						"signup"
					],
					"query": [
						{
							"key": "username",
							"value": "teste",
							"disabled": true
						},
						{
							"key": "password",
							"value": "teste",
							"disabled": true
						}
					]
				}
			},
			"response": []
		},
		{
			"name": "GET DATA",
			"event": [
				{
					"listen": "prerequest",
					"script": {
						"exec": [
							"const toISOString = date => date.toISOString();",
							"var start_timestamp = toISOString(new Date(\"2024-04-24T10:24:05Z\"))",
							"pm.globals.set(\"start_timestamp\", start_timestamp);",
							"",
							"var end_timestamp = toISOString(new Date(\"2024-04-24T10:24:05Z\"))",
							"pm.globals.set(\"end_timestamp\", end_timestamp);"
						],
						"type": "text/javascript",
						"packages": {}
					}
				}
			],
			"protocolProfileBehavior": {
				"disableBodyPruning": true
			},
			"request": {
				"auth": {
					"type": "bearer",
					"bearer": [
						{
							"key": "token",
							"value": "",
							"type": "string"
						}
					]
				},
				"method": "GET",
				"header": [],
				"body": {
					"mode": "formdata",
					"formdata": []
				},
				"url": {
					"raw": "http://localhost:8080/api/data?start=2024-04-25T07:40:33Z&end=2024-04-25T07:40:33Z&skip=0&limit=100",
					"protocol": "http",
					"host": [
						"localhost"
					],
					"port": "8080",
					"path": [
						"api",
						"data"
					],
					"query": [
						{
							"key": "start",
							"value": "2024-04-25T07:40:33Z"
						},
						{
							"key": "end",
							"value": "2024-04-25T07:40:33Z"
						},
						{
							"key": "skip",
							"value": "0"
						},
						{
							"key": "limit",
							"value": "100"
						}
					]
				}
			},
			"response": []
		},
		{
			"name": "GET POPULATE",
			"request": {
				"auth": {
					"type": "bearer",
					"bearer": [
						{
							"key": "token",
							"value": "",
							"type": "string"
						}
					]
				},
				"method": "GET",
				"header": [],
				"url": {
					"raw": "http://localhost:8080/api/populate",
					"protocol": "http",
					"host": [
						"localhost"
					],
					"port": "8080",
					"path": [
						"api",
						"populate"
					]
				}
			},
			"response": []
		}
	]
}
```