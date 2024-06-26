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