#!/bin/bash

echo "Создаю сеть"

# Переменная с именем сети
NETWORK_NAME="network-aerial-photography"

if docker network inspect $NETWORK_NAME &> /dev/null; then
  echo "Сеть уже существует: $NETWORK_NAME"
else
  # Создание сети
  docker network create $NETWORK_NAME

  # Проверка успешного создания сети
  if [ $? -eq 0 ]; then
    echo "Сеть успешно создана: $NETWORK_NAME"
  else
    echo "Ошибка при создании сети"
    exit 1
  fi
fi

docker-compose --env-file .env -f ./docker/server/docker-compose.yaml up --build