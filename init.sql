CREATE DATABASE data_points_db;
\connect data_points_db;

CREATE TABLE "users" (
  "id" integer PRIMARY KEY,
  "username" varchar NOT NULL,
  "password" varchar NOT NULL,
  "role" varchar NOT NULL,
  "created_at" timestamp
);

CREATE TABLE "data_points" (
  "id" integer PRIMARY KEY,
  "time" timestamp NOT NULL,
  "value" DOUBLE PRECISION NOT NULL,
  "valid" boolean NOT NULL,
  "tags" varchar[],
  "created_at" timestamp
);
