FROM --platform=linux/amd64 python:3.9 as build

WORKDIR /app

COPY . /app

RUN pip install flask
RUN pip install requests
RUN pip install psycopg2


CMD ["python", "log_output.py"]