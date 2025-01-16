FROM python:3.10

WORKDIR /app

COPY todo_backend.py /app/

RUN pip install flask
RUN pip install psycopg2


EXPOSE 5000

CMD ["python", "todo_backend.py"]
