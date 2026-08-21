FROM python:3.11-slim

WORKDIR /app

COPY services/common /app/services/common
COPY services/analyzer /app/services/analyzer
RUN touch /app/services/__init__.py

RUN pip install --no-cache-dir -r /app/services/analyzer/requirements.txt

WORKDIR /app
ENV PYTHONPATH=/app
EXPOSE 8000

CMD ["uvicorn", "services.analyzer.main:app", "--host", "0.0.0.0", "--port", "8000"]
