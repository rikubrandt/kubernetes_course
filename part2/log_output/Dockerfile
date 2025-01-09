FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install flask
RUN pip install requests



CMD ["python", "log_output.py"]