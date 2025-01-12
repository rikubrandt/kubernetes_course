FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install flask
RUN pip install requests
RUN pip install psycopg2


CMD ["python", "log_output.py"]