FROM python:3.9-slim

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip setuptools wheel

COPY aerial_photography /app/aerial_photography

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

CMD uvicorn aerial_photography.app:app --reload --workers 1 --host 0.0.0.0 --port 8000