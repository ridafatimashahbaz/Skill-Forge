FROM python:3.11-slim

WORKDIR /app
COPY services /app/services
COPY scripts /app/scripts
RUN touch /app/services/__init__.py

RUN pip install --no-cache-dir \
    sqlalchemy==2.0.35 psycopg2-binary==2.9.9 \
    chromadb==0.5.5

ENV PYTHONPATH=/app
