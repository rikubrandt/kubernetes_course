FROM python:3.10-slim

WORKDIR /app

COPY todo_backend.py /app/

RUN pip install flask

EXPOSE 5000

CMD ["python", "todo_backend.py"]
