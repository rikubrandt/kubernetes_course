FROM --platform=linux/amd64 python:3.9 as build

WORKDIR /app

COPY todo_backend.py /app/

RUN pip install flask
RUN pip install psycopg2


EXPOSE 5000

CMD ["python", "todo_backend.py"]
