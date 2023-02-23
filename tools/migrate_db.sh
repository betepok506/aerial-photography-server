#!/bin/bash

docker-compose --env-file .env.migrations -f ./docker/migrations/docker-compose.yaml up --build