#!/bin/bash

docker-compose --env-file .env -f ./docker/server/docker-compose.yaml up --build