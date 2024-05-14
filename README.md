# FastAPI template

Проект развернут на удаленном сервере по адресу:<br>
https://.duckdns.org/api/v1 <br>
https://.duckdns.org/api/v2 <br>


Администрирование приложения может быть осуществлено:
  - через админ панель по адресу https://.duckdns.org/admin <br>
      <a href="#t1">Учетные данные</a> для входа в админ-зону
  - через Swagger доступный по адресу https://.duckdns.org/docs

Техническая документация:
  - Redoc доступен по адресу https://.duckdns.org/redoc
  - Скачать yaml-файл можно по адресу https://.duckdns.org/schema


<br>

## Оглавление
- [Технологии](#технологии)
- [Описание работы](#описание-работы)
- [Установка приложения](#установка-приложения)
- [Запуск тестов](#запуск-тестов)
- [Запуск приложения](#запуск-приложения)
- [Удаление приложения](#удаление-приложения)
- [Автор](#автор)

<br>

## Технологии
<details><summary>Подробнее</summary><br>

[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/-FastAPI-464646?logo=fastapi)](https://fastapi.tiangolo.com/)
[![FastAPI_Users](https://img.shields.io/badge/-FastAPI--Users-464646?logo=fastapi-users)](https://fastapi-users.github.io/fastapi-users/)
[![Pydantic](https://img.shields.io/badge/pydantic-2.7-blue?logo=Pydantic)](https://docs.pydantic.dev/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?logo=PostgreSQL)](https://www.postgresql.org/)
[![asyncpg](https://img.shields.io/badge/-asyncpg-464646?logo=PostgreSQL)](https://pypi.org/project/asyncpg/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-blue?logo=sqlalchemy)](https://www.sqlalchemy.org/)
[![Alembic](https://img.shields.io/badge/-Alembic-464646?logo=alembic)](https://alembic.sqlalchemy.org/en/latest/)
[![Uvicorn](https://img.shields.io/badge/-Uvicorn-464646?logo=Uvicorn)](https://www.uvicorn.org/)
[![docker_compose](https://img.shields.io/badge/-Docker%20Compose-464646?logo=docker)](https://docs.docker.com/compose/)
[![docker_hub](https://img.shields.io/badge/-Docker_Hub-464646?logo=docker)](https://hub.docker.com/)
[![GitHub_Actions](https://img.shields.io/badge/-GitHub_Actions-464646?logo=GitHub)](https://docs.github.com/en/actions)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?logo=NGINX)](https://nginx.org/en/docs/)
[![SWAG](https://img.shields.io/badge/-SWAG-464646?logo=swag)](https://docs.linuxserver.io/general/swag)
[![httpx](https://img.shields.io/badge/-httpx-464646?logo=httpx)](https://www.python-httpx.org/)
[![Pytest](https://img.shields.io/badge/-Pytest-464646?logo=Pytest)](https://docs.pytest.org/en/latest/)
[![Pytest-asyncio](https://img.shields.io/badge/-Pytest--asyncio-464646?logo=Pytest-asyncio)](https://pypi.org/project/pytest-asyncio/)
[![pytest-cov](https://img.shields.io/badge/-pytest--cov-464646?logo=codecov)](https://pytest-cov.readthedocs.io/en/latest/)
[![deepdiff](https://img.shields.io/badge/-deepdiff-464646?logo=deepdiff)](https://zepworks.com/deepdiff/7.0.1/)
[![pre-commit](https://img.shields.io/badge/-pre--commit-464646?logo=pre-commit)](https://pre-commit.com/)

[⬆️Оглавление](#оглавление)

</details>

<br>

## Описание работы:
Add app description here

<br>

## Установка приложения:

<details><summary>Предварительные условия</summary>

Предполагается, что пользователь установил [Docker](https://docs.docker.com/engine/install/) и [Docker Compose](https://docs.docker.com/compose/install/) на локальной машине. Проверить наличие можно выполнив команды:

```bash
docker --version && docker-compose --version
```
</details>

<br>

Клонируйте репозиторий с GitHub и введите данные для переменных окружения (значения даны для примера, но их можно оставить):

```bash
git clone https://github.com/alexpro2022/shift_FastAPI.git
cd shift_FastAPI
cp .env.example .env
nano .env
```

[⬆️Оглавление](#оглавление)

<br>

## Запуск тестов:
Из корневой директории проекта выполните команду запуска тестов:
```bash
docker compose -f docker/test/docker-compose.yml --env-file .env up --build --abort-on-container-exit && \
docker compose -f docker/test/docker-compose.yml --env-file .env down -v && docker system prune -f
```
После прохождения тестов в консоль будет выведен отчет pytest и coverage.

[⬆️Оглавление](#оглавление)

<br>

## Запуск приложения:

1. Из корневой директории проекта выполните команду:
```bash
docker compose -f docker/dev/docker-compose.yml --env-file .env up -d --build
```
  Проект будет развернут в docker-контейнерах по адресу http://localhost:8000

  Администрирование приложения может быть осуществлено:
  - через Swagger доступный по адресу http://localhost:8000/docs
  - через админ панель по адресу http://localhost:8000/admin

  <h4 id="t1">Учетные данные для входа в админ-зону:</h4>
    <ul>
      <li>login: adm@adm.com
      <li>password: admpw
    </ul><br>

  Техническая документация:
  - Swagger доступен по адресу http://localhost:8000/docs
  - Redoc доступен по адресу http://localhost:8000/redoc

<br>
2. Остановить docker и удалить контейнеры можно командой из корневой директории проекта:

```bash
docker compose -f docker/dev/docker-compose.yml --env-file .env down
```

Если также необходимо удалить том базы данных:
```bash
docker compose -f docker/dev/docker-compose.yml --env-file .env down -v && docker system prune -f
```

[⬆️Оглавление](#оглавление)

<br>

## Удаление приложения:
Из корневой директории проекта выполните команду:
```bash
cd .. && rm -fr shift_FastAPI
```

[⬆️Оглавление](#оглавление)

<br>

## Автор:
[Aleksei Proskuriakov](https://github.com/alexpro2022)

[⬆️В начало](#FastAPI-template)
