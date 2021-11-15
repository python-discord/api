FROM python:3.9.5-slim-buster as base

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VERSION=1.1.5 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    INSTALL_DIR="/opt/dependencies" \
    APP_DIR="/app"

ENV PATH="$POETRY_HOME/bin:$INSTALL_DIR/.venv/bin:$PATH"

RUN groupadd -g 61000 api \
 && useradd -g 61000 -l -r -u 61000 api

FROM base as builder
RUN apt-get update \
  && apt-get -y upgrade \
  && apt-get install --no-install-recommends -y \
  curl \
  build-essential

RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

WORKDIR $INSTALL_DIR
COPY "pyproject.toml" "poetry.lock" ./
RUN poetry install --no-dev

FROM base as development
WORKDIR $APP_DIR
ENV FASTAPI_ENV=development
COPY --from=builder $INSTALL_DIR $INSTALL_DIR

COPY . .
CMD ["sh", "-c", "alembic upgrade head && uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload"]

FROM base as production
ENV FASTAPI_ENV=production
COPY --from=builder $INSTALL_DIR $INSTALL_DIR

WORKDIR $APP_DIR
COPY . .
RUN python -m compileall api/

USER api
CMD ["sh", "-c", "alembic upgrade head && gunicorn"]