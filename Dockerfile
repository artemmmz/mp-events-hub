FROM python:3.13-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

ADD pyproject.toml uv.lock /app/

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

COPY app /app

RUN uv sync --frozen