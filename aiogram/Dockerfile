FROM python:3.12.3-slim AS base

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY aiogram/requirements.txt .


FROM base AS dev
RUN pip install --no-cache-dir --upgrade -r requirements.txt


FROM base AS prod
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY aiogram .