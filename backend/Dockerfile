# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.10.6
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

ENV DOCKER="true"

WORKDIR /app

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

RUN mkdir -p /data
RUN chown -R appuser:appuser /data

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

USER appuser

COPY . .

EXPOSE 8000

CMD uvicorn 'app.main:app' --host=0.0.0.0 --port=8000