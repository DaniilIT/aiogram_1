FROM python:3.11-alpine

WORKDIR /bot_app

RUN apk update && \
    apk add make

RUN pip install --upgrade setuptools && \
    pip install poetry

COPY pyproject.toml ./

RUN poetry config virtualenvs.create false && \
    poetry install --without dev --no-ansi --no-interaction --no-root

COPY . .

CMD make migrate && \
    cd bot && \
    python main.py
