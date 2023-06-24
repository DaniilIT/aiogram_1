# aiogram bot

Проект для изучения aiogram, асинхронного фреймворка управления telegram bot. \
В проекте используются базы данных PostgreSQL и redis.
Все handlers подключаются через router в файле `bot/handlers/__init__.py`.
Middleware заносит новых пользователей в базу данных.


## Установка и настройка

Зависимости указаны в файле `pyproject.toml`, установите их командами:

```sh
pip install poetry && poetry install
```

### Конфигурация

Создайте в корневой папке проекта файл `.env` по шаблону `.env.example`, где:

* LOG_LEVEL – уровень логирования (DEBUG/INFO/WARNING/ERROR)
* DB_ECHO - логирование запросов в базу данных
* TG_TOKEN – токен в https://core.telegram.org/bots/
* DB_USER - пользователь postgresql
* DB_PASS - пароль postgresql
* DB_NAME - база данных postgresql
* DB_HOST - хост postgresql
* DB_PORT - порт postgresql
* REDIS_PASS - пароль redis
* REDIS_HOST - хост redis
* REDIS_PORT - порт redis


## Запуск

Запустите базы данных PostgreSQL и Redis:

```sh
docker-compose up -d postgres
docker-compose up -d redis
```

Накатите миграции:

```sh
make migrate
```

Запустите бота:

```sh
cd bot
python main.py
```


## Цели проекта

Код написан в учебных целях.


## Лицензия

Этот проект лицензирован в соответствии с условиями лицензии MIT.
