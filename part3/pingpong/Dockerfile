FROM --platform=linux/amd64 python:3.9 as build
WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir flask requests psycopg2 requests

CMD ["python", "ping_pong.py"]