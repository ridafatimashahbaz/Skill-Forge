FROM python:3.11-slim

WORKDIR /app

COPY services/common /app/services/common
COPY services/auth /app/services/auth
RUN touch /app/services/__init__.py

RUN pip install --no-cache-dir -r /app/services/auth/requirements.txt

WORKDIR /app
ENV PYTHONPATH=/app
EXPOSE 8000

CMD ["uvicorn", "services.auth.main:app", "--host", "0.0.0.0", "--port", "8000"]
