FROM python:3.9-slim

WORKDIR /app
COPY alembic.ini /app/alembic.ini
COPY database/models.py /app/database/models.py
RUN pip3 install --no-cache-dir alembic psycopg2-binary

CMD alembic upgrade head && alembic revision --autogenerate && alembic upgrade head