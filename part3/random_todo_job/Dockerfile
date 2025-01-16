FROM python:3.10-slim
WORKDIR /app
COPY add_random_todo.py /app/
RUN pip install requests
CMD ["python", "/app/add_random_todo.py"]
