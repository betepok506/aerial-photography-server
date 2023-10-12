#!/bin/bash

#set -e
#set -x
# Linux
#set PYTHONPATH=.

# Windows
#export PYTHONPATH=.

#pytest --cov=aerial_photography --cov-report=term-missing aerial_photography/tests "${@}"

docker-compose --env-file .env -f ./docker/tests/docker-compose.yaml config > docker-stack.yml

docker-compose -f docker-stack.yml build
docker-compose -f docker-stack.yml down -v --remove-orphans # Remove possibly previous broken stacks left hanging after an error
docker-compose -f docker-stack.yml up -d
chmod +x $(pwd)/aerial_photography/tests-start.sh

docker-compose -f docker-stack.yml exec -T aerial-photography-backend bash aerial_photography/tests-start.sh
#docker-compose -f docker-stack.yml down -v --remove-orphans